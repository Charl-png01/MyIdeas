from passlib.hash import pbkdf2_sha256
import time
all_pass_lex = [''.join(c) for c in product(letters, repeat=5)]
random.shuffle(all_pass_lex)
# Function to compute the PBKDF2 hash of a password with a given salt
def pbkdf2_hash(password, salt, iterations=29000):
    return pbkdf2_sha256.using(salt=salt.encode('utf-8'), rounds=iterations).hash(password)

# Brute-force attack
start_time = time.time()
for hash_entry in hashes:
    parts = hash_entry.split('$')
    if len(parts) != 4:
        print(f"Invalid hash entry format: {hash_entry}")
        continue

    _, _, salt, target_hash = parts

    for candidate in all_pass_lex:
        hashed_candidate = pbkdf2_hash(candidate, salt)
        if hashed_candidate == target_hash:
            end_time = time.time()
            print(f"Cracked Password: {candidate}")
            print(f"Hash: {target_hash}")
            print(f"Time Taken: {end_time - start_time:.2f} seconds")
            break
    else:
        print("Password not found for hash:", target_hash)
