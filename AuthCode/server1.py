import socket
import threading
import sys
import datetime
import time
import binascii
import struct
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

# Helper functions to load keys
def load_public_key(file):
    with open(file, "rb") as infile:
        public_key = serialization.load_pem_public_key(infile.read())
    return public_key

def load_private_key(file, password=None):
    with open(file, "rb") as infile:
        private_key = serialization.load_pem_private_key(infile.read(), password)
    return private_key

# Load keys
server_public_key = load_public_key("public_key.pem")
client_private_key = load_private_key("private_key.pem")

print_lock = threading.Lock()  # mutex lock for display access

def print_msg(msg):
    '''
    Print a message with current timestamp
    msg: the message string
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")

def handle_client(client_socket, client_ip, client_port):
    print_msg("Connection from " + client_ip + ":" + client_port)

    # Receive the size of the client message
    try:
        client_msg_size = struct.unpack("!I", client_socket.recv(4))[0]
    except struct.error as e:
        print_msg("Error receiving client message size: " + str(e))
        return

    # Receive the client message
    client_message = bytearray()
    while len(client_message) < client_msg_size:
        chunk = client_socket.recv(min(4096, client_msg_size - len(client_message)))
        if not chunk:
            break
        client_message.extend(chunk)

    # Check if the client message is long enough to contain the client nonce
    if len(client_message) < 512:
        print_msg("Error: Client message too short to contain client nonce")
        return

    # Split the client message
    encrypted_client_nonce = client_message[:32]
    encrypted_session_key = client_message[32:]

    # Decrypt encrypted_client_nonce using client's private key
    try:
        client_nonce = client_private_key.decrypt(
            encrypted_client_nonce,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        print_msg("Error decrypting client nonce: " + str(e))
        return

    # Generate a random 256-bit server nonce
    server_nonce = os.urandom(32)

    # Compute the hash of nonces
    digest = hashes.Hash(hashes.SHA256())
    digest.update(client_nonce)
    digest.update(server_nonce)
    hash_value = digest.finalize()

    # Encrypt server_nonce with client's public key using OAEP padding
    encrypted_server_nonce = server_public_key.encrypt(
        server_nonce,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    server_message = encrypted_server_nonce + encrypted_session_key + hash_value

    # Send the size of the server message
    server_msg_size = len(server_message)
    client_socket.sendall(struct.pack("!I", server_msg_size))

    # Send the server message to the client
    client_socket.sendall(server_message)

    print_msg("Connection closed to " + client_ip + ":" + client_port)
    client_socket.close()

# Main server code
if __name__ == '__main__':
    host = '127.0.0.1'  # IP address to accept connections
    port = 5000  # Port number to accept connections

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    # Allow only five clients at a time
    server_socket.listen(5)

    print_msg("Listening for connection on " + host + ":" + str(port))

    while True:
        try:
            client_socket, address = server_socket.accept()  # Accept new connection
            client_ip = address[0]
            client_port = str(address[1])

            # Start a thread to handle client connection
            threading.Thread(target=handle_client, args=(client_socket, client_ip, client_port), daemon=True).start()

        except KeyboardInterrupt:  # Handle CTRL+C
            print("")
            print_msg("Server stopped")
            break
        except Exception as e:
            print_msg("Exception: " + str(e))
            break



