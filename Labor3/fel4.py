#4. A titkosított állomány Hill módszerrel volt rejtjelezve, ahol a blokk méret d = 2 és a titkosítást a bájtok felett végezték (mod 256-al kell számolni!!). Tudva azt, hogy az "0x28 0x03"-nek "0x09 0xb7" és "0xff 0xd9"-nek "0xac 0xfb" a rejtjele határozzuk meg az eredeti jpeg állományt.
import numpy as np

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_inverse(matrix, mod):
    det = int((matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]) % mod)
    det_inv = mod_inverse(det, mod)

    result = np.zeros((2, 2), dtype=int)
    result[0, 0] = (matrix[1, 1] * det_inv) % mod
    result[0, 1] = ((-matrix[0, 1]) * det_inv) % mod
    result[1, 0] = ((-matrix[1, 0]) * det_inv) % mod
    result[1, 1] = (matrix[0, 0] * det_inv) % mod
    return result

# Known plaintext-ciphertext pairs
p1, c1 = [0x28, 0x03], [0x09, 0xb7]
p2, c2 = [0xff, 0xd9], [0xac, 0xfb]

# Create matrices and find encryption key
P = np.array([[p1[0], p2[0]], [p1[1], p2[1]]])
C = np.array([[c1[0], c2[0]], [c1[1], c2[1]]])
P_inv = matrix_mod_inverse(P, 256)

K = np.zeros((2, 2), dtype=int)
for i in range(2):
    for j in range(2):
        K[i, j] = sum((C[i, k] * P_inv[k, j]) % 256 for k in range(2)) % 256

# Get decryption key
K_inv = matrix_mod_inverse(K, 256)
print(f"K =\n{K}\nK^-1 =\n{K_inv}")

# Decrypt file
with open("cryptHill", 'rb') as f:
    data = f.read()

result = bytearray()
for i in range(0, len(data), 2):
    if i + 1 < len(data):
        c = [data[i], data[i+1]]
        p = [
            (K_inv[0, 0] * c[0] + K_inv[0, 1] * c[1]) % 256,
            (K_inv[1, 0] * c[0] + K_inv[1, 1] * c[1]) % 256
        ]
        result.extend(p)

with open("decryptedHill.jpg", 'wb') as f:
    f.write(result)

print("Decryption complete.")
