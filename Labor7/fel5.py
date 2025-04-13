from sympy.polys.polytools import gcdex
import binascii
import math
from sympy import gcd

# Read the keys
with open('key_e.txt', 'r') as f:
    lines = f.readlines()
    n = int(lines[0].strip())
    e = int(lines[1].strip())

with open('key_f.txt', 'r') as f:
    lines = f.readlines()
    n_check = int(lines[0].strip())
    f = int(lines[1].strip())

# Verify both files have the same modulus
assert n == n_check, "Modulus values in the two key files do not match!"

# Read the encrypted files
with open('RSAcr1', 'rb') as file:
    cnr1_bytes = file.read()
    cnr1 = int.from_bytes(cnr1_bytes, byteorder='big')

with open('RSAcr2', 'rb') as file:
    cnr2_bytes = file.read()
    cnr2 = int.from_bytes(cnr2_bytes, byteorder='big')

# Extended Euclidean algorithm to find x and y such that e*x + f*y = 1
x, y, g = gcdex(e, f)

# Convert sympy types to Python integers
x = int(x)
y = int(y)

# Ensure we have a valid solution
assert g == 1, "The exponents are not coprime!"

# Calculate original message
# m ≡ (cnr1^x * cnr2^y) mod n
m = (pow(cnr1, x, n) * pow(cnr2, y, n)) % n

# Convert message to bytes
message_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')

# Save the decrypted message
with open('decrypted_message.txt', 'wb') as f:
    f.write(message_bytes)

# Print the result
try:
    message = message_bytes.decode('utf-8')
    print(f"Decrypted message: {message}")
except UnicodeDecodeError:
    print(f"Couldn't decode as UTF-8. Hex representation: {binascii.hexlify(message_bytes)}")
