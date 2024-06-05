import socket
import struct
import datetime
import time
import binascii
import os
import threading
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

print_lock = threading.Lock()  # mutex lock for display access

def print_msg(msg, client_nonce=None):
    '''
    Print a message with current timestamp
    msg: the message string
    client_nonce: the client nonce (optional)
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")
        if client_nonce:
            print("Client nonce: " + str(binascii.hexlify(client_nonce)))

# Function to establish session key
def establish_session_key(client_socket, server_public_key, client_private_key):
    # Generate a random nonce (client nonce)
    client_nonce = os.urandom(32)

    # Encrypt the client nonce using the server's public key
    encrypted_client_nonce = server_public_key.encrypt(
        client_nonce,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send the size of the encrypted nonce to the server
    client_msg_size = len(encrypted_client_nonce)
    client_socket.sendall(struct.pack("!I", client_msg_size))

    # Send the encrypted nonce to the server
    client_socket.sendall(encrypted_client_nonce)
    print(encrypted_client_nonce)

    # Receive the size of the server message
    try:
        server_msg_size = struct.unpack("!I", client_socket.recv(4))[0]
    except struct.error as e:
        print_msg("Error receiving server message size: " + str(e))
        return None

    # Receive the server message
    server_message = bytearray(32)
    while len(server_message) < server_msg_size:
        chunk = client_socket.recv(server_msg_size - len(server_message))
        if not chunk:
            break
        server_message.extend(chunk)

    # Check if server message size is valid
    if len(server_message) != server_msg_size:
        print_msg("Error: Invalid server message size")
        return None

    # Split the server message
    encrypted_server_nonce = server_message[:32]  # Assuming nonce length is 32
    encrypted_session_key = server_message[32:]
    print(encrypted_session_key)
    hash_value = server_message[64:]

    # Decrypt encrypted_server_nonce using client's private key
    try:
        server_nonce = client_private_key.decrypt(
            encrypted_server_nonce,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(encrypted_session_key)
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

    # Decrypt encrypted_session_key using client's private key
    try:
        session_key = client_private_key.decrypt(
            bytes(encrypted_session_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("session key" + session_key)
    except ValueError as e:
        print_msg("Error decrypting session key: " + str(e))
        return None

    return session_key

# Main client code
if __name__ == '__main__':
    host = '127.0.0.1'  # server ip
    port = 5000         # server port

    # Load server's public key from a file
    with open("public_key.pem", "rb") as key_file:
        server_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Load client's private key from the new file (private_key.pem)
    with open("private_key.pem", "rb") as key_file:
        client_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

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
    session_key = establish_session_key(client_socket, server_public_key, client_private_key)
    if session_key:
        print_msg("Established session key: " + str(session_key))

    # Close the connection
    if client_socket:
        client_socket.close()
        print_msg("Client stopped")
    sys.exit(0)


