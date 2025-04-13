#1. A PasswdSHA256.txt állományban személyek nevei és jelszavaiknak hash értéke található. A hash értékek az SHA3-256-os hash függvényt alkalmazva voltak létrehozva. Határozzuk meg melyek azok a személyek, amelyeknek ugyanaz a jelszava.
import json

# Read the password file
with open('PasswdSHA256.txt', 'r') as f:
    lines = f.readlines()

# Parse the data and organize by password hash
users_by_hash = {}
for line in lines:
    if line.strip():  # Skip empty lines
        user_data = eval(line.strip())  # Parse the dictionary
        name = user_data['name']
        password_hash = user_data['password']
        
        if password_hash in users_by_hash:
            users_by_hash[password_hash].append(name)
        else:
            users_by_hash[password_hash] = [name]

# Find and display users with the same password
print("Users with the same password:")
for password_hash, users in users_by_hash.items():
    if len(users) > 1:
        print(f"These users have the same password:")
        for user in users:
            print(f"  - {user}")
        print()
