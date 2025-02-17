import socket
import threading
import sys
import datetime
import time
import binascii
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Helper functions
def load_public_key(file):
    with open(file, "rb") as infile:
        public_key = serialization.load_pem_public_key(infile.read())
    return public_key

def load_private_key(file, password=None):
    with open(file, "rb") as infile:
        private_key = serialization.load_pem_private_key(infile.read(), password)
    return private_key

# Load keys
client_public_key = load_public_key("client_public_key.pem")
server_private_key = load_private_key("server_private_key.pem")

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
    '''
    Handles connection from a client
    client_socket: socket to use to read/write to client
    client_ip:     IP address of client
    client_port:   port number of client connection
    '''
    print_msg("Connection from " + client_ip + ":" + client_port)

    # Receive the client message
    # Receive the client message
    client_message = bytearray()
    expected_message_length = 1024  # Total expected message length

    while len(client_message) < expected_message_length:
        chunk = client_socket.recv(expected_message_length - len(client_message))
        if not chunk:
            break
        client_message.extend(chunk)

    # Decrypt encrypted_client_nonce using server's private key
    encrypted_client_nonce = client_message[:32]  # Assuming fixed nonce length
    encrypted_client_nonce_padded = encrypted_client_nonce.ljust(1024, b'\0')

    # Decrypt the padded encrypted nonce
    try:
        client_nonce = server_private_key.decrypt(
            bytes(encrypted_client_nonce_padded),
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

    # Encrypt server_nonce with client's public key using OAEP padding
    encrypted_server_nonce = client_public_key.encrypt(
        server_nonce,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Ensure that the encrypted server nonce is padded to a fixed length
    encrypted_server_nonce_padded = encrypted_server_nonce.ljust(expected_message_length, b'\0')

    # Concatenate encrypted_server_nonce_padded, encrypted_session_key, and hash value
    server_message = encrypted_server_nonce_padded + encrypted_session_key + hash_value

    # Send the server message to the client
    client_socket.sendall(server_message)

    # Decrypt encrypted_session_key using server's private key
    try:
        client_nonce = client_private_key.decrypt(
            client_nonce,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        print_msg("Error decrypting client nonce: " + str(e))
        return

    # Print session key
    if session_key is None:
        print_msg("No session key established!")
    else:
        print_msg("Established session key: " + str(binascii.hexlify(session_key)))

    # Close the connection (must always be done)
    if client_socket:
        client_socket.close()
    print_msg("Connection closed to " + client_ip + ":" + client_port)


if __name__ == '__main__':
    host = '127.0.0.1'  # ip to use to accept connections
    port = 5000  # port number to use to accept connections

    # Create a server socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    # Allow only five clients at a time
    server_socket.listen(5)

    print_msg("Listening for connection on " + host + ":" + str(port))

    while True:
        try:
            client_socket, address = server_socket.accept()  # accept new connection
            client_ip = address[0]
            client_port = str(address[1])

            # Start a thread to handle client connection
            threading.Thread(target=handle_client, args=(client_socket, client_ip, client_port), daemon=True).start()

        except KeyboardInterrupt:  # CTRL+C
            print("")
            print_msg("Server stopped")

            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(0)
        except Exception as e:
            print_msg("Exception: " + str(e))

            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(1)
