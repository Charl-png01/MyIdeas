from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    # Generate an RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize the private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize the public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

def save_to_pem_files(private_pem, public_pem, private_file="private_key.pem", public_file="public_key.pem"):
    # Save the private key to a PEM file
    with open(private_file, "wb") as private_key_file:
        private_key_file.write(private_pem)

    # Save the public key to a PEM file
    with open(public_file, "wb") as public_key_file:
        public_key_file.write(public_pem)

if __name__ == "__main__":
    private_pem, public_pem = generate_key_pair()
    save_to_pem_files(private_pem, public_pem)
    print("RSA key pair generated and saved to 'private_key.pem' and 'public_key.pem'.")

