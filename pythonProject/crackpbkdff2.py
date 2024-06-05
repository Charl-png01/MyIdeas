import hashlib
import time
import random
from string import ascii_lowercase as letters
from itertools import product
from passlib.hash import pbkdf2_sha256
import os


# Function to compute the SHA256 hash of a password with a given salt
def sha256_hash(password, salt):
    password_bytes = password.encode('utf-8')
    salt_bytes = bytes.fromhex(salt)
    hash_obj = hashlib.sha256()
    hash_obj.update(salt_bytes + password_bytes)
    return hash_obj.hexdigest()


# Function to perform a brute-force attack for a single hash
def brute_force_single_hash(hash_entry, all_pass_lex):
    salt, target_hash = hash_entry.split('$')
    for candidate in all_pass_lex:
        if sha256_hash(candidate, salt) == target_hash:
            return candidate
    return None
# this code maybe commented in order for the sha256 to work.
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



# Function to calculate average ATC and TTC for a list of hashes
def calculate_average_atc_ttc(hash_file, method):
    with open(hash_file, 'r') as hash_file:
        hashes = hash_file.read().splitlines()

    total_attempts = 0
    total_time = 0

    for hash_entry in hashes:
        start_time = time.time()
        cracked_password = brute_force_single_hash(hash_entry, all_pass_lex)
        end_time = time.time()

        total_time += (end_time - start_time)
        total_attempts += 1

        if cracked_password is not None:
            print(f"Cracked Password (Method {method}): {cracked_password}")
            print(f"Hash: {hash_entry.split('$')[-1]}")

    avg_attempts = total_attempts / len(hashes)
    avg_ttc = total_time / len(hashes)

    return avg_attempts, avg_ttc


# Read the hash files
hash_file1 = 'sha256_hash1.txt'
hash_file2 = 'sha256_hash2.txt'

# Create a list of all possible passwords in lexicographically sorted order
all_pass_lex = [''.join(c) for c in product(letters, repeat=5)]

# Shuffle the list for random method
random.shuffle(all_pass_lex)

# Calculate average ATC and TTC for hash_file1 using the random method
avg_attempts1_random, avg_ttc1_random = calculate_average_atc_ttc(hash_file1, "Random")
print(f"Average ATC for {hash_file1} (Random): {avg_attempts1_random}")
print(f"Average TTC for {hash_file1} (Random): {avg_ttc1_random:.2f} seconds")

# Reset the list to lexicographical order
all_pass_lex = [''.join(c) for c in product(letters, repeat=5)]

# Calculate average ATC and TTC for hash_file1 using the lexicographical method
avg_attempts1_lex, avg_ttc1_lex = calculate_average_atc_ttc(hash_file1, "Lexicographical")
print(f"Average ATC for {hash_file1} (Lexicographical): {avg_attempts1_lex}")
print(f"Average TTC for {hash_file1} (Lexicographical): {avg_ttc1_lex:.2f} seconds")

