import socket
import ssl
import threading
import subprocess
import sys
import struct
import hashlib

from subprocess import check_output

from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
from pytun import Error as pytunError

from pypacker.layer3.ip import IP as IPv4Packet
from pypacker.pypacker import DissectException

from utils import print_packet_meta, print_msg


# The following four variables should be set to None 
# when no client is connected
client_socket = None              # the SSL socket after client connects
client_remote_ip = None           # IP of connected client
client_tunnel_remote_ip = None    # tunnel remote IP of connected client
client_tunnel_local_ip = None     # tunnel local IP for connected client 

PBKDF2_HMAC_ROUNDS = 100000    # number of rounds used in PBKDF2


# A dummy password database arranged as a dictionary
# { username: [salt, PBKDF2 hash], ... }
pwd_dummy_db = {'alice': [b"\xb9\xfa\x0bk\x83\xcd(tX\x1e\x08\xf28\xa9\x1c+\x923M\xa8\xd0V\xd7\x92\x93jX'e\xa1F\xda", b"\xcb\x17\xd3\xb5]\x98\xad\xa6\x93\xcfd\xbf\x1cg\xea?q\xd8\x1b\x89\xa1\xb3\x105\xafQ\xde\x8a\xd3f1\x11"]}


def authenticate():
    # TODO: See assignment description
    '''
    Obtain login and password from user, verify, and send response

    Note: use client_socket to send response through SSL channel

    Return True or False depending on authentication success or failure
    
    '''
    global client_socket

    # Receive login credentials from client
    try:
        credentials = client_socket.recv(1024).decode().strip().split(":")
        username = credentials[0]
        password = credentials[1]

        # Hash the password using PBKDF2
        salt = pwd_dummy_db.get(username, [None, None])[0]
        if salt is None:
            return False
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_HMAC_ROUNDS)

        # Compare hashed password with stored hash
        stored_hash = pwd_dummy_db.get(username, [None, None])[1]
        if hashed_password != stored_hash:
            return False

        # Send authentication success message to client
        client_socket.sendall("Authenticated".encode())
        return True
    except Exception as e:
        print("Error during authentication:", e)
        return False


def tun_to_ssl():
    # TODO: See assignment description
    '''
    Read packets from TUN interface, change destination IP, package, 
    and write to SSL channel

    Note: use client_socket to write data to SSL channel

    Note: this function starts running in a thread as soon as the server
          starts, irrespective of whether a client is connected or not; the
          implementation has to handle exceptions when trying to write data
          to the SSL channel as a client may not be connected, or a client
          may disconnect arbitrarily 
    '''
    global client_socket

    if client_socket is None:
        print("client socket iss not initialised")
        return

    while True:
        try:
            # Read a packet from the TUN interface
            packet = tun.read(tun.mtu)

            # Package the packet
            packet_size = len(packet)
            packet_size_data = struct.pack("!i", packet_size)

            # Send packet size
            client_socket.sendall(packet_size_data)

            # Send the packet
            client_socket.sendall(packet)
        except Exception as e:
            print("Error in tun_to_ssl thread:", e)
            return

def ssl_to_tun():
    # TODO: See assignment description
    '''
    Read data from SSL channel, unpackage, change source IP in packets, 
    and write packets to TUN interface

    Note: use client_socket to read data from SSL channel

    Note: runs in a thread after a client connects; the implemantation has to
          catch exceptions when reading data from the channel, and accordingly
          close the connection and return
    '''
    global client_socket

    while True:
        try:
            # Read data from the SSL channel
            packet_size_data = client_socket.recv(4)
            packet_size = struct.unpack("!i", packet_size_data)[0]
            packet = client_socket.recv(packet_size)

            # Change source IP in the packet
            try:
                ipv4_packet = IPv4Packet(packet)
                ipv4_packet.src_s = client_tunnel_remote_ip
                packet = ipv4_packet.bin()
            except DissectException:
                print("Not an IPv4 packet")

            # Write the modified packet to the TUN interface
            tun.write(packet)

        except ssl.SSLError as e:
            print("SSL Error :", e)
        except ConnectionResetErroronn as e:
            print("ConnectionResetError :", e)
        except ConnectionAbortedError as e:
            print("ConnectionAbortedError :", e)
    

if __name__ == '__main__':

    host = '192.199.1.10'  # IP to use to accept connections
    port = 5000            # port number to use to accept connections

    # Check if in server network or not
    this_ip = check_output(['hostname', '--all-ip-address']).strip().decode()
    if this_ip != host:
        print_msg("You are not in the server network")
        sys.exit(1)

    # Create onion-remote TUN interface
    try:
        tun = TunTapDevice(name='onion-remote', flags=(IFF_TUN | IFF_NO_PI))
        tun.addr = '10.10.1.1'
        tun.netmask = '255.255.255.0'
        tun.mtu = 1500
        tun.up()
    except pytunError as e:
        print_msg("Error creating TUN device...server may be already running" + str(e))
        sys.exit(1) 

    # Start thread to monitor incoming packets in TUN interface
    threading.Thread(target=tun_to_ssl, daemon=True).start()

    # Create a regular server socket
    # Create a regular server socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    # Allow only one client at a time
    server_socket.listen(1)

    #TODO Set up server to receive TLS connections 
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="tunnelserver.crt", keyfile="tunnelserver_pubpri.pem")
    tls_server_socket = context.wrap_socket(server_socket, server_side=True)

    print_msg("Listening for connection on " + host + ":" + str(port))

    # Initialize client_socket here
    client_socket = None

    while True:
        try:
            client_socket, address = tls_server_socket.accept()  # accept new connection
            client_remote_ip = address[0]
            client_remote_port = str(address[1])

            print_msg("Connection from " + client_remote_ip + ":" + client_remote_port)

            # Authenticate client
            if authenticate() == False:
                print_msg("Authentication failed from " + client_remote_ip + ":" + client_remote_port)
                if client_socket:
                    client_socket.close()
                client_socket = None
                client_remote_ip = None
                client_tunnel_remote_ip = None
                client_tunnel_local_ip = None
                continue  # go back to waiting for another connection

            print_msg("Authenticated " + client_remote_ip + ":" + client_remote_port)

            # Assign tunnel IPs and start thread to monitor SSL channel
            client_tunnel_local_ip = "10.0.0.2"
            client_tunnel_remote_ip = "10.10.1.2"
            threading.Thread(target=ssl_to_tun, daemon=True).start()

        except ssl.SSLError as e:
            print_msg("SSL Error: " + e.reason)

        except KeyboardInterrupt:  # CTRL+C
            print("")
            print_msg("Server stopped")
            if tls_server_socket:
                tls_server_socket.close()
            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            tun.close()
            sys.exit(0)
