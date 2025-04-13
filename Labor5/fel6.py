import numpy as np
from PIL import Image
import io

# Main parameters
key = np.array([[27, 131], [22, 101]])
key_inv = np.array([[1, 57], [162,127]])
iv = (129, 131)

def decrypt_block(cb, pb):
    cb = [int(c) for c in cb]
    pb = [int(p) for p in pb]

    decrypted = np.dot(key_inv, cb) % 256
    plain = [int(decrypted[0]) ^ pb[0], int(decrypted[1]) ^ pb[1]]
    return bytes(plain)

def decrypt_gif(encrypted_data):
    blocks = [encrypted_data[i:i+2] for i in range(0, len(encrypted_data), 2)]
    plain = bytearray()

    prev = iv
    for cb in blocks:
        if len(cb) == 1:
            cb += bytes([0])
        decrypted = decrypt_block(cb, prev)
        plain.extend(decrypted)
        prev = cb
    return bytes(plain)

# Decrypt the GIF file
with open('cryptHillCBC_TheCircleIsComplete', 'rb') as f:
    encrypted_data = f.read()

decrypted_data = decrypt_gif(encrypted_data)

with open('decrypted.gif', 'wb') as f:
    f.write(decrypted_data)