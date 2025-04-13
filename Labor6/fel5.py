import json
import hashlib
import base64
import bcrypt
import time

# Load the password hashes and salts from previous task
with open('PasswdSHA256Salt.json', 'r') as f:
    users = json.load(f)

# Load common passwords list
with open('10-million-password-list-top-10000.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

# Find users with common passwords (reusing code from fel4.py)
cracked_users = []

for user in users:
    name = user['name']
    stored_password_hash = base64.b64decode(user['password'])
    salt = base64.b64decode(user['salt'])
    
    for password in common_passwords:
        # Calculate hash using the same parameters
        password_bytes = password.encode('utf-8')
        calculated_hash = hashlib.pbkdf2_hmac(
            'sha3_256',
            password_bytes,
            salt,
            1000,
            len(stored_password_hash)
        )
        
        # Compare the calculated hash with the stored hash
        if calculated_hash == stored_password_hash:
            cracked_users.append({
                "name": name,
                "password": password,
                "salt": user['salt']
            })
            print(f"Found password for {name}: {password}")
            break

# Create a new JSON with bcrypt hashes for cracked users
bcrypt_users = []

for user in cracked_users:
    name = user['name']
    password = user['password']
    
    # bcrypt generates its own salt, but we'll store the original salt as well
    password_bytes = password.encode('utf-8')
    bcrypt_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    
    bcrypt_users.append({
        "name": name,
        "password": bcrypt_hash.decode('utf-8'),
        "salt": user['salt']  # Original salt kept for reference
    })

# Save the bcrypt hashes to a JSON file
with open('BcryptPasswords.json', 'w') as f:
    json.dump(bcrypt_users, f, indent=4)

print(f"\nExported {len(bcrypt_users)} bcrypt password hashes to BcryptPasswords.json")

# Now try to crack these bcrypt passwords
print("\nAttempting to crack bcrypt passwords...")

# Only cracking the first user for demonstration
if bcrypt_users:
    first_user = bcrypt_users[0]
    name = first_user['name']
    stored_bcrypt_hash = first_user['password'].encode('utf-8')
    
    # Track timing for cracking attempt
    start_time = time.time()
    found = False
    
    # Try the first 100 passwords (to avoid very long runtime)
    max_attempts = 100
    for i, password in enumerate(common_passwords[:max_attempts]):
        if i % 10 == 0:
            print(f"Trying password {i+1}/{max_attempts}...")
            
        password_bytes = password.encode('utf-8')
        if bcrypt.checkpw(password_bytes, stored_bcrypt_hash):
            end_time = time.time()
            print(f"Found password for {name}: {password}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            found = True
            break
    
    if not found:
        end_time = time.time()
        print(f"Password not found in {max_attempts} attempts.")
        print(f"Time taken for {max_attempts} attempts: {end_time - start_time:.2f} seconds")
        
        # Extrapolate how long it would take to check all 10,000 passwords
        time_per_password = (end_time - start_time) / max_attempts
        total_estimated_time = time_per_password * 10000
        print(f"Estimated time to check all 10,000 passwords: {total_estimated_time:.2f} seconds")
        print(f"({total_estimated_time/60:.2f} minutes or {total_estimated_time/3600:.2f} hours)")

print("\nConclusion: bcrypt is designed to be slow and resistant to brute force attacks.")
print("It includes work factor parameter that can be increased as hardware gets faster.")
print("This makes password cracking significantly more time-consuming and resource-intensive.")
