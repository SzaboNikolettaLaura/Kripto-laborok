# 2. A crypted7_2.png AES-GCM módszerrel volt rejtjelezve. Határozzuk meg az eredeti png filet, ha az AES 32 bájtos kulcs titkosított értékét hexában cryptedAESkey7_2.txt-ben találjuk. Az AES kulcs RSA-OAEP-vel volt titkosítva, ahol az RSA publikus kulcs az RSA_pubKey7_2.pem állományban található.
# Megjegyzések:

# a további hitelesített bájtszekvencia, a header:
# AES_GCMEncryption 2025.04.01,
# a nonce értéke a titkosított állomány első 12 bájtja,
# a hitelesítő tag pedig a titkosított állomány utolsó 16 bájtja.
# Útmutatás: faktorizáljuk az RSA publikus kulcs modulusát Fermat módszerével.
import math
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import binascii

# Function to perform Fermat factorization
def fermat_factorization(n):
    a = math.isqrt(n) + 1
    b2 = a*a - n
    while not is_perfect_square(b2):
        a += 1
        b2 = a*a - n
    b = math.isqrt(b2)
    return a + b, a - b

def is_perfect_square(n):
    root = math.isqrt(n)
    return root * root == n

# Read encrypted PNG file
with open('crypted7_2.png', 'rb') as f:
    encrypted_data = f.read()

# Read encrypted AES key
with open('cryptedAESkey7_2.txt', 'r') as f:
    encrypted_aes_key_hex = f.read().strip()
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key_hex)

# Read RSA public key
with open('RSA_pubKey7_2.pem', 'rb') as f:
    rsa_key = RSA.import_key(f.read())

# Extract RSA public key components
n = rsa_key.n
e = rsa_key.e

# Factorize n using Fermat's method
p, q = fermat_factorization(n)

# Construct the private key
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# Create the private key object
private_key = RSA.construct((n, e, d, p, q))

# Decrypt the AES key using RSA-OAEP
cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# Extract nonce and tag from encrypted data
# The nonce is the first 12 bytes and the tag is the last 16 bytes
nonce = encrypted_data[:12]
ciphertext = encrypted_data[12:-16]
tag = encrypted_data[-16:]

# Header for authentication
header = b"AES_GCMEncryption 2025.04.01"

# Decrypt the file using AES-GCM
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
cipher.update(header)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)

# Write the decrypted data to a file
with open('decrypted7_2.png', 'wb') as f:
    f.write(plaintext)

print("Decryption complete. The decrypted file has been saved as 'decrypted7_2.png'.")
