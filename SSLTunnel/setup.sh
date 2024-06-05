#!/bin/bash

set -e

#### Cleanup old settings, if any

# Check if processes already in server network
if [[ $(sudo ip netns list | grep server-net) ]] 
then
    if [[ ! -z $(sudo ip netns pids server-net) ]]
    then
        echo "One or more processes are running through a server terminal."
        read -p "Force close all (y/n)?" sel
        case $sel in
            [yY]* ) sudo ip netns pids server-net | sudo xargs kill;;
            * ) exit 0
        esac
    fi
fi

# Check if processes already in client network
if [[ $(sudo ip netns list | grep client-net) ]] 
then
    if [[ ! -z $(sudo ip netns pids client-net) ]]
    then
        echo "One or more processes are running through a client terminal."
        read -p "Force close all (y/n)?" sel
        case $sel in
            [yY]* ) sudo ip netns pids client-net | sudo xargs kill;;
            * ) exit 0
        esac
    fi
fi

# Delete networks
sudo ip -all netns del 2> /dev/null || true

# Delete links
sudo ip link set veth-cw down 2> /dev/null || true
sudo ip link del veth-cw 2> /dev/null || true
sudo ip link set veth-sw down 2> /dev/null || true
sudo ip link del veth-sw 2> /dev/null || true


# Clean up iptables, if any
sudo iptables -t nat -D POSTROUTING -s 172.16.1.0/24 -j SNAT --to 172.16.1.1 2> /dev/null || true
sudo iptables -t nat -D POSTROUTING -s 192.199.1.0/24 -j SNAT --to 192.199.1.1 2> /dev/null || true
sudo iptables -t nat -D PREROUTING -d 192.199.1.1/32 -p tcp --dport 5000 -j DNAT --to-destination 192.199.1.10:5000 2> /dev/null || true
sudo iptables -D FORWARD -i veth-cw -j ACCEPT 2> /dev/null || true
sudo iptables -D FORWARD -o veth-cw -j ACCEPT 2> /dev/null || true
sudo iptables -D FORWARD -i veth-sw -j ACCEPT 2> /dev/null || true
sudo iptables -D FORWARD -o veth-sw -j ACCEPT 2> /dev/null || true

#### Do setup

# Create two network namespaces
echo -n "Creating network namespaces..."
sudo ip netns add client-net
sudo ip netns add server-net
echo "OK"

echo -n "Creating virtual links..."
# Create virtual interface pairs to connect client machine and world (VM)
# One end is called eth0-c and the other end veth-cw (gateway)
sudo ip link add eth0-c type veth peer name veth-cw

# Create virtual interface pairs to connect server machine and world (VM)
# One end is called eth0-s and the other end veth-sw (gateway)
sudo ip link add eth0-s type veth peer name veth-sw
echo "OK"

# Assign interfaces to namespace (eth0-c to client-net and eth0-s to server-net)
echo -n "Adding link ends to networks..."
sudo ip link set eth0-c netns client-net
sudo ip link set eth0-s netns server-net
echo "OK"

# Activate root interfaces
echo -n "Configuring root network..."
#echo "    turning links up"
sudo ip link set veth-cw up
sudo ip link set veth-sw up
#echo "    assigning gateway IP addresses"
sudo ip address add 172.16.1.1/24 dev veth-cw
sudo ip address add 192.199.1.1/24 dev veth-sw
#echo "    setting up forwarding"
sudo sysctl -wq net.ipv4.ip_forward=1 
sudo sysctl -wq net.ipv4.conf.veth-cw.forwarding=1
sudo sysctl -wq net.ipv4.conf.veth-sw.forwarding=1
sudo iptables -A FORWARD -i veth-cw -j ACCEPT
sudo iptables -A FORWARD -o veth-cw -j ACCEPT
sudo iptables -A FORWARD -i veth-sw -j ACCEPT
sudo iptables -A FORWARD -o veth-sw -j ACCEPT
#echo "    setting up iptables"
# Source nat-ting all traffic from client network to gateway address
sudo iptables -t nat -A POSTROUTING -s 172.16.1.0/24 -j SNAT --to 172.16.1.1
# Source nat-ting all traffic from server network to gateway address
sudo iptables -t nat -A POSTROUTING -s 192.199.1.0/24 -j SNAT --to 192.199.1.1
# Port forward from gateway to server machine in server network at port 5000
sudo iptables -t nat -A PREROUTING -d 192.199.1.1/32 -p tcp --dport 5000 -j DNAT --to-destination 192.199.1.10:5000
#echo "    creating net namespace directories"
sudo mkdir -p /etc/netns/client-net
sudo mkdir -p /etc/netns/server-net
echo "OK"

# Activate client network
echo -n "Configuring client network..."
# Turn on interfaces
sudo ip netns exec client-net ip link set dev lo up
sudo ip netns exec client-net ip link set dev eth0-c up
# Assign IP address and default route via gateway
sudo ip netns exec client-net ip address add 172.16.1.10/24 dev eth0-c
sudo ip netns exec client-net ip route add default via 172.16.1.1 dev eth0-c metric 100
# Set up DNS server for server machine as 8.8.8.8
sudo ip netns exec client-net bash -c "echo 'nameserver 8.8.8.8' > /etc/netns/client-net/resolv.conf"
# Add static route to server network via client gateway (this is required because the default route will be overwritten once tunnel is created)
sudo ip netns exec client-net ip route add 192.199.1.1/32 via 172.16.1.1 dev eth0-c 
echo "OK"

# Activate server network
echo -n "Configuring server network..."
sudo ip netns exec server-net ip link set dev lo up
sudo ip netns exec server-net ip link set dev eth0-s up
sudo ip netns exec server-net ip address add 192.199.1.10/24 dev eth0-s
sudo ip netns exec server-net ip route add default via 192.199.1.1 dev eth0-s metric 100
sudo ip netns exec server-net bash -c "echo 'nameserver 8.8.8.8' > /etc/netns/server-net/resolv.conf"
# Replace source IP of all packets from 10.10.1.0/24 to server eth0-s IP
sudo ip netns exec server-net iptables -t nat -A POSTROUTING -s 10.10.1.0/24 -j MASQUERADE
echo "OK"






