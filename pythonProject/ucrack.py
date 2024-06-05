import hashlib
import time
import random
from string import ascii_lowercase, ascii_letters
from itertools import product
from passlib.hash import pbkdf2_sha256

# Function to crack a PBKDF2 hash using a specified method
def crack_pbkdf2(hash_value, method):
    # Implement cracking logic for PBKDF2 hashes
    if method == 'pbkdf2':
        parts = hash_value.split('$')
        if len(parts) != 4 or parts[0] != '$pbkdf2-sha256':
            print(f"Invalid hash entry format: {hash_value}")
            return None

        # Extract the salt and target hash
        salt, target_hash = parts[2:]

        # Brute-force attack with randomly chosen passwords
        for candidate in all_pass_lex:
            hashed_candidate = pbkdf2_sha256.using(salt=salt, rounds=29000).hash(candidate)
            if hashed_candidate == target_hash:
                return candidate
    return None

# Read the hash file
with open('pbkdf2_hash2.txt', 'r') as hash_file:
    hashes = hash_file.read().splitlines()

# Create a list of all possible passwords and shuffle it
all_pass_lex = [''.join(c) for c in product(ascii_lowercase, repeat=5)]
random.shuffle(all_pass_lex)

# Brute-force attack
start_time = time.time()
for hash_entry in hashes:
    cracked_password = crack_pbkdf2(hash_entry, 'pbkdf2')
    if cracked_password is not None:
        end_time = time.time()
        print(f"Cracked Password: {cracked_password}")
        print(f"Hash: {hash_entry}")
        print(f"Time Taken: {end_time - start_time:.2f} seconds")
    else:
        print("Password not found for hash:", hash_entry)
