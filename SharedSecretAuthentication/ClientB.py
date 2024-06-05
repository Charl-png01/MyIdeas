import os
import hmac
import hashlib
import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Function to generate DH key pair
def generate_dh_key_pair():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Function to compute shared secret
def compute_shared_secret(private_key, peer_public_key):
    shared_secret = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_secret)
    return derived_key

# Function to generate HMAC
def generate_hmac(key, nonce):
    return hmac.new(key, nonce, hashlib.sha256).digest()

def main():
    # Generate DH key pairs
    private_key_b, public_key_b = generate_dh_key_pair()

    # Serialize public key to send to A
    pu_b_bytes = public_key_b.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Simulate sending public key to A and receiving A's public key (over a secure channel)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        s.sendall(b'PUB_KEY_B,' + pu_b_bytes)
        data = s.recv(1024)
        if data.startswith(b'PUB_KEY_A,'):
            pu_a_bytes = data[len('PUB_KEY_A,'):]
            peer_public_key_a = serialization.load_pem_public_key(pu_a_bytes, backend=default_backend())

    # Compute shared secret
    shared_secret_b = compute_shared_secret(private_key_b, peer_public_key_a)

    # Generate nonce
    nonce_b = os.urandom(16)

    # Generate HMAC
    hmac_b = generate_hmac(shared_secret_b, nonce_b)

    # Send first 20 bits of HMAC and nonce to the trusted node
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        s.sendall(b'B,' + hmac_b[:3] + b',' + nonce_b)
        result = s.recv(1024)
        if result == b'MATCH':
            print("HMACs match, proceeding with nonce exchange")
            # Simulate exchanging nonces with A (over a secure channel)
            nonce_a = b''  # Received from A
            if hmac.compare_digest(generate_hmac(shared_secret_b, nonce_a), hmac_b):
                print("Shared secret verified successfully!")
            else:
                print("Shared secret verification failed.")
        else:
            print("HMACs do not match, potential MITM attack detected.")

if __name__ == "__main__":
    main()

