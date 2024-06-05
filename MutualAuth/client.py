import socket
import threading
import sys
import datetime
import time
import binascii
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

print_lock = threading.Lock()  # mutex lock for display access

def load_server_private_key(file, password=None):
    with open(file, "rb") as infile:
        private_key = serialization.load_pem_private_key(infile.read(), password)
    return private_key

def load_client_public_key(file):
    with open(file, "rb") as infile:
        public_key = serialization.load_pem_public_key(infile.read())
    return public_key

def print_msg(msg):
    '''
    Print a message with current timestamp
    msg: the message string
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")

def establish_session_key(client_socket, server_public_key, server_private_key):
    # Generate a random nonce (client nonce)
    client_nonce = os.urandom(32)

    # Encrypt the client nonce using the server's public key
    encrypted_client_nonce = server_public_key.encrypt(
        bytes(client_nonce),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    expected_message_length = 1024
    encrypted_client_nonce_padded = encrypted_client_nonce.ljust(expected_message_length, b'\0')

    # Send the encrypted nonce to the server
    client_socket.sendall(encrypted_client_nonce_padded)

    # Receive the server message
    server_message = client_socket.recv(1024)

    # Split the server message
    encrypted_server_nonce = server_message[:32]
    encrypted_session_key = server_message[32:]
    hash_value = server_message[64:]

    # Decrypt encrypted_server_nonce using server's private key
    try:
        server_nonce = server_private_key.decrypt(
            bytes(encrypted_client_nonce),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        print_msg("Error decrypting server nonce: " + str(e))
        return None

    # Verify hash of nonces
    digest = hashes.Hash(hashes.SHA256())
    digest.update(client_nonce)
    digest.update(server_nonce)
    computed_hash = digest.finalize()
    if computed_hash != hash_value:
        print_msg("Error: Hash of nonces does not match")
        return None

    # Decrypt encrypted_session_key using server's private key
    try:
        session_key = server_private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    except ValueError as e:
        print_msg("Error decrypting session key: " + str(e))
        return None

    return session_key

if __name__ == '__main__':
    host = '127.0.0.1'  # server ip
    port = 5000         # server port

    # Load server's public key from a file
    with open("server_public_key.pem", "rb") as key_file:
        server_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Load server's private key from a file
    server_private_key = load_server_private_key("server_private_key.pem")

    # Create a regular client socket
    client_socket = socket.socket()

    # Establish connection with server
    print_msg("Establishing connection to " + host + ":" + str(port))

    try:
        client_socket.connect((host, port))  # connect to the server
    except Exception as e:
        print_msg("Error during connection: " + str(e))
        sys.exit(1)

    # Establish session key
    session_key = establish_session_key(client_socket, server_public_key, server_private_key)

    if session_key:
        print_msg("Established session key: " + str(session_key))

    # Close the connection
    client_socket.close()
    print_msg("Client stopped")
    sys.exit(0)
