import socket
import ssl
import threading
import subprocess
import struct
import sys
import getpass

from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
from pytun import Error as pytunError

from pypacker.layer3.ip import IP as IPv4Packet
from pypacker.pypacker import DissectException

from utils import print_packet_meta, print_msg

def tunnel_all():
    '''
    Route all traffic via onion-local (this program)
    '''
    subprocess.run("sudo ip route add default via 10.0.0.2 dev onion-local src 172.16.1.10 metric 0", shell=True)
    
    subprocess.run("sudo iptables -t nat -A POSTROUTING -o onion-local -j MASQUERADE", shell=True)


def tunnel_net(nets):
    '''
    Route selective network traffic via onion-local (this program)
    nets: list of destination networks (CIDR notation) for which traffic 
          should be routed
    '''
    for net in nets:
        subprocess.run("sudo ip route add " + net + " dev onion-local src 172.16.1.10", shell=True)

    subprocess.run("sudo iptables -t nat -A POSTROUTING -o onion-local -j MASQUERADE", shell=True)


def authenticate(sock):
    # TODO: See assignment description
    '''
    Obtain login and password from user, send to server, and get response
    sock: socket to use to send data to server

    Return True or False depending on authentication success or failure
    
    '''
    username = input("Login: ")
    password = getpass.getpass("Password: ")

    # Send login credentials to server
    try:
        sock.sendall(f"{username}:{password}".encode())

        # Receive response from server
        response = sock.recv(1024).decode().strip()

        # Check if authentication succeeded
        if response == "Authenticated":
            return True
        else:
            return False
    except Exception as e:
        print("Error during authentication:", e)
        return False

def tun_to_ssl(sock):
    # TODO: See assignment description
    '''
    Read packets from TUN interface, package, and write to SSL channel
    sock: SSL socket to write packaged data to

    Note: runs in a thread
    '''
    if sock is None:
        return

    try:
        while True:
            # Read a packet from the TUN interface
            packet = tun.read(tun.mtu)

            # Package the packet
            packet_size = len(packet)
            packet_size_data = struct.pack("!i", packet_size)

            # Send packet size
            sock.sendall(packet_size_data)

            # Send the packet
            sock.sendall(packet)
    except Exception as e:
        print("Error in tun_to_ssl thread:", e)
        return

def ssl_to_tun(sock):
    # TODO: See assignment description
    '''
    Read data from SSL channel, unpackage, and write packets to TUN interface
    sock: SSL socket to read packaged data from

    Note: runs in a thread
    '''
    int_size = struct.calcsize("!i")

    if sock is None:
        return

    try:
        while True:
            # Read the packet size from the SSL channel
            packet_size_data = sock.recv(int_size)
            if len(packet_size_data) < int_size:
                break
            packet_size = struct.unpack("!i", packet_size_data)[0]

            # Read the packet from the SSL channel
            packet = sock.recv(packet_size)

            # Write the packet to the TUN interface
            tun.write(packet)
    except Exception as e:
        print("Error in ssl_to_tun thread:", e)
        return

if __name__ == '__main__':
    host = '172.16.1.10'    # client's regular ip
    server = '192.199.1.1'  # tunnel server ip
    port = 5000             # tunnel server port

    # Check if in client network or not
    this_ip = subprocess.check_output(['hostname', '--all-ip-address']).strip().decode()
    if this_ip != host:
        print_msg("You are not in the client network")
        sys.exit(1)

    # Create onion-local TUN interface
    try:
        tun = TunTapDevice(name='onion-local', flags=(IFF_TUN | IFF_NO_PI))
        tun.addr = '10.0.0.2'
        tun.netmask = '255.255.255.0'
        tun.mtu = 1500
        tun.up() 
    except pytunError:
        print_msg("Error creating TUN device...client may be already running")
        sys.exit(1)

    # Create a regular client socket
    client_socket = socket.socket()      
    client_socket.bind(('172.16.1.10',0)) 

    # TODO: Set up TLS connection to server
    # Set up SSL context for server authentication
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="ultimateca.crt")
    tls_client_socket = context.wrap_socket(client_socket, server_hostname='server')

    # Run authentication
    if authenticate(tls_client_socket) == False:
        print_msg("Authentication failed")
        sys.exit(1)

    # Create threads to read/write from/to TUN interface
    print_msg("Authentication successful")
    t1 = threading.Thread(target=ssl_to_tun, args=(tls_client_socket,), daemon=True)
    t2 = threading.Thread(target=tun_to_ssl, args=(tls_client_socket,), daemon=True)

    # Send all local traffic through SSL channel
    # Use tunnel_net() to selectively send traffic, e.g. tunnel_net(['130.253.0.0/16'])
    tunnel_all() 

    # Start threads
    t1.start()
    t2.start()

    # Wait for threads to end, or keyboard interrupt (Ctrl+C)
    try:
        t1.join()
    except KeyboardInterrupt:
        print("")
    finally:
        print_msg("Client stopped")
        if tls_client_socket:
            tls_client_socket.close()
        if client_socket:
            client_socket.close()
        tun.close()
        sys.exit(0)
    
    
