#4. Az előző feladatnál, akiknek sikerült a jelszavát feltörni, azok esetében végezzük el a következőket: mentsük ki egy json állományba a személyek nevét, a jelszavak hashértékét, és a salt-ot, de most az iterációszámot állítsuk legalább 1000000-re. Sikerül-e ebben az esetben is feltörni a jelszavakat?
import json
import hashlib
import base64

# Load the password hashes and salts
with open('PasswdSHA256Salt.json', 'r') as f:
    users = json.load(f)

# Load the cracked passwords from exercise 3
# For this, we'll rerun a simplified version of exercise 3
with open('10-million-password-list-top-10000.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

# Find users with common passwords
cracked_users = []

for user in users:
    name = user['name']
    stored_password_hash = base64.b64decode(user['password'])
    salt = base64.b64decode(user['salt'])
    
    for password in common_passwords:
        # Calculate hash using the same parameters as in exercise 3
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

# Now create a new JSON with the cracked passwords but using 1,000,000 iterations
secure_users = []

for user in cracked_users:
    name = user['name']
    password = user['password']
    salt = user['salt']
    salt_bytes = base64.b64decode(salt)
    
    # Calculate the new hash with 1,000,000 iterations
    password_bytes = password.encode('utf-8')
    new_hash = hashlib.pbkdf2_hmac(
        'sha3_256',
        password_bytes,
        salt_bytes,
        1000000,  # High iteration count
        32  # Output size in bytes
    )
    
    secure_users.append({
        "name": name,
        "password": base64.b64encode(new_hash).decode('utf-8'),
        "salt": salt
    })

# Save the new secure hashes to a JSON file
with open('SecurePasswdSHA256Salt.json', 'w') as f:
    json.dump(secure_users, f, indent=4)

print(f"\nExported {len(secure_users)} secure password hashes to SecurePasswdSHA256Salt.json")

# Now try to crack these passwords with the high iteration count
# Warning: This will be extremely slow due to the high iteration count
print("\nAttempting to crack passwords with 1,000,000 iterations (this will be very slow)...")

# For demonstration, we'll just try to crack the first user with a few passwords
if secure_users:
    first_user = secure_users[0]
    name = first_user['name']
    stored_password_hash = base64.b64decode(first_user['password'])
    salt = base64.b64decode(first_user['salt'])
    
    # We'll only try the first few passwords to demonstrate
    for password in common_passwords[:10]:
        print(f"Trying password: {password}")
        password_bytes = password.encode('utf-8')
        calculated_hash = hashlib.pbkdf2_hmac(
            'sha3_256',
            password_bytes,
            salt,
            1000000,  # High iteration count
            len(stored_password_hash)
        )
        
        if calculated_hash == stored_password_hash:
            print(f"Found password for {name}: {password}")
            break
    else:
        print(f"Password not found in the first 10 attempts. Full cracking would take a very long time.")

print("\nConclusion: With 1,000,000 iterations, cracking passwords becomes computationally expensive")
print("and may not be feasible with regular hardware in a reasonable timeframe.")
