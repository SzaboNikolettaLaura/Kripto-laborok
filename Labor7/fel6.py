#6. A crypted7_6.jpg AES-CBC módszerrel volt rejtjelezve, ahol az alkalmazott iv a titkosított file első 16 bájtja. Határozzuk meg az eredeti jpg filet, ha az AES 32 bájtos kulcs titkosított értékét hexában a cryptedAESkey7_6.txt-ben találjuk. Az AES kulcs RSA-OAEP-vel volt titkosítva, ahol az RSA privát kulcs az RSA_privKey7_6.pem állományban található, és adott az állományhoz való hozzáférési jelszó SHA256-os értéke: 591a6e49ad819403426545301221da1764be6c58727b18831cc7d4bf8dbff4e9.
import hashlib
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

# Check which password matches the given SHA256 hash
target_hash = "591a6e49ad819403426545301221da1764be6c58727b18831cc7d4bf8dbff4e9"
possible_passwords = ["myPassword000", "problem7_6", "password2025", "myPass2025", "password7_6"]

correct_password = None
for password in possible_passwords:
    password_bytes = password.encode('utf-8')
    h = hashlib.sha256(password_bytes).hexdigest()
    if h == target_hash:
        correct_password = password
        print(f"Found correct password: {correct_password}")
        break

if not correct_password:
    print("No matching password found")
    exit(1)

# Load RSA private key with the password
key_path = "RSA_privKey7_6 (1).pem"
with open(key_path, "rb") as f:
    private_key = RSA.import_key(f.read(), passphrase=correct_password)

# Create RSA cipher object for decryption
rsa_cipher = PKCS1_OAEP.new(private_key)

# Read the encrypted AES key
with open("cryptedAESkey7_6 (1).txt", "rb") as f:
    encrypted_aes_key = bytes.fromhex(f.read().decode().strip())

# Decrypt the AES key
aes_key = rsa_cipher.decrypt(encrypted_aes_key)
print(f"AES key length: {len(aes_key)} bytes")

# Read the encrypted image file
with open("crypted7_6.jpg", "rb") as f:
    encrypted_data = f.read()

# Extract IV (first 16 bytes) and ciphertext
iv = encrypted_data[:16]
ciphertext = encrypted_data[16:]

# Decrypt the image
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(ciphertext)

# Save the decrypted image
with open("decrypted7_6.jpg", "wb") as f:
    f.write(decrypted_data)

print("Image successfully decrypted and saved as 'decrypted7_6.jpg'")
