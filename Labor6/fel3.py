#3. A PasswdSHA256Salt.json állományban személyek nevei, jelszavaiknak hash értéke és a megfelelő salt értékek találhatók. A hash értékek a Python hashlib.pbkdf2_hmac kulcs deriváló függvényével voltak létrehozva, ahol az alkalmazott hash függvény az SHA3-256-os volt és az iterációszám csak 1000-re volt állítva. Tudva, hogy néhány személyeknek jelszava a leggyakrabban használt jelszavak közül került ki, határozzuk meg ezeket a személyeket, illetve a jelszavaikat. A leggyakrabban használt jelszavakat a 10-million-password-list-top-10000.txt állományban találjuk.
import json
import hashlib
import base64

# Load the password hashes and salts
with open('PasswdSHA256Salt.json', 'r') as f:
    users = json.load(f)

# Load the common passwords list
with open('10-million-password-list-top-10000.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

# Find users with common passwords
found_users = []

for user in users:
    name = user['name']
    stored_password_hash = base64.b64decode(user['password'])
    salt = base64.b64decode(user['salt'])
    
    for password in common_passwords:
        # Calculate hash using the same parameters as mentioned in the task
        password_bytes = password.encode('utf-8')
        calculated_hash = hashlib.pbkdf2_hmac(
            'sha3_256',  # using SHA3-256
            password_bytes,
            salt,
            1000,        # iteration count
            len(stored_password_hash)
        )
        
        # Compare the calculated hash with the stored hash
        if calculated_hash == stored_password_hash:
            found_users.append({
                "name": name,
                "password": password
            })
            print(f"Found password for {name}: {password}")
            break

print(f"\nTotal users with common passwords found: {len(found_users)}")
for user in found_users:
    print(f"{user['name']}: {user['password']}")
