#2. A PasswdSHA256.json állományban személyek nevei és jelszavaiknak hash értéke található. A hash értékek az SHA3-256-os hash függvényt alkalmazva voltak létrehozva. Tudva, hogy néhány személy jelszava a leggyakrabban használt jelszavak közül került ki, határozzuk meg ezeket a személyeket, illetve a jelszavaikat. A leggyakrabban használt jelszavakat a 10-million-password-list-top-10000.txt állományban találjuk.
import json
import hashlib
import base64

# Load password hashes
with open('PasswdSHA256.json', 'r') as f:
    users = json.load(f)

# Load common passwords
with open('10-million-password-list-top-10000.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

# Function to hash a password using SHA3-256
def hash_password(password):
    hash_obj = hashlib.sha3_256(password.encode())
    return base64.b64encode(hash_obj.digest()).decode()

# Check each common password against all user hashes
found_users = []

for password in common_passwords:
    hashed_password = hash_password(password)
    
    for user in users:
        if user["password"] == hashed_password:
            found_users.append({
                "name": user["name"],
                "password": password
            })

# Print results
print("Users with common passwords:")
for user in found_users:
    print(f"{user['name']}: {user['password']}")
