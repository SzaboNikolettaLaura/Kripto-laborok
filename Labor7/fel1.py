#1. Válasszunk két, legalább 1024 bites prímszámot, majd RSA-kulcsként alkalmazva őket titkosítsunk és fejtsünk vissza egy tetszőleges ASCII karaktereket tartalmazó szöveget. A szöveget generáljuk véletlenszerűen, hossza pedig akkor legyen, hogy a szövegnek megfelelő szám kisebb legyen, mint az RSA-modulus. Ugyanazt a szöveget titkosítsuk többször RSA-val, majd RSA-OAEP-vel. A titkosított bájtszekvenciákat hexa formában írjuk ki a képernyőre. A titkosított bájtszekvenciákat megfigyelve mit lehet megállapítani?
import random
import string
import math
from Crypto.Util.number import getPrime, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

# Generate two random primes of at least 1024 bits
p = getPrime(1024)
q = getPrime(1024)

# Calculate modulus and RSA parameters
n = p * q
phi = (p - 1) * (q - 1)
e = 65537  # Common public exponent
d = inverse(e, phi)  # Private exponent

# Print key information
print(f"RSA Modulus (n) bit length: {n.bit_length()}")

# Function to generate random text
def generate_random_text(max_length):
    # Calculate maximum safe length to ensure the number is smaller than modulus
    safe_length = (n.bit_length() // 8) - 1
    length = min(max_length, safe_length)
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ') for _ in range(length))

# Plain RSA encryption
def rsa_encrypt(message):
    # Convert message to integer
    m = int.from_bytes(message.encode('ascii'), byteorder='big')
    # Ensure message is smaller than modulus
    if m >= n:
        raise ValueError("Message too long for this key")
    # Encrypt: c = m^e mod n
    c = pow(m, e, n)
    return c

# Plain RSA decryption
def rsa_decrypt(ciphertext):
    # Decrypt: m = c^d mod n
    m = pow(ciphertext, d, n)
    # Convert integer back to bytes and then to ASCII
    byte_length = (m.bit_length() + 7) // 8
    return m.to_bytes(byte_length, byteorder='big').decode('ascii', errors='ignore')

# Create RSA key object for OAEP
key = RSA.construct((n, e, d, p, q))

# RSA-OAEP encryption
def rsa_oaep_encrypt(message):
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(message.encode('ascii'))

# RSA-OAEP decryption
def rsa_oaep_decrypt(ciphertext):
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(ciphertext).decode('ascii')

# Generate random message (ensuring it's smaller than modulus)
message = generate_random_text(100)
print(f"\nOriginal message: {message}")

# Encrypt the message multiple times with plain RSA
print("\nPlain RSA Encryption (multiple runs):")
for i in range(3):
    rsa_encrypted = rsa_encrypt(message)
    print(f"Run {i+1}: {hex(rsa_encrypted)}")
    
    # Verify decryption works
    if i == 0:
        decrypted = rsa_decrypt(rsa_encrypted)
        print(f"Decrypted message: {decrypted}")
        assert decrypted == message, "RSA decryption failed!"

# Encrypt the message multiple times with RSA-OAEP
print("\nRSA-OAEP Encryption (multiple runs):")
for i in range(3):
    oaep_encrypted = rsa_oaep_encrypt(message)
    print(f"Run {i+1}: {binascii.hexlify(oaep_encrypted).decode()}")
    
    # Verify decryption works
    if i == 0:
        decrypted = rsa_oaep_decrypt(oaep_encrypted)
        print(f"Decrypted message: {decrypted}")
        assert decrypted == message, "RSA-OAEP decryption failed!"

print("\nObservation: Plain RSA encryption of the same message always produces the same ciphertext,")
print("while RSA-OAEP produces different ciphertexts each time due to random padding.")
