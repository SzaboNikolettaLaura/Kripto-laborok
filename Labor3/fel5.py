#5. Írjunk programot, amely titkosít és visszafejt egy tetszőleges bináris állományt, ahol blokkonként a Hill-256 titkosítót alkalmazzuk, ahol tetszőlegesen lehessen blokkméretet változtatni, és oldjuk meg az utolsó blokk paddingolását, a PKCS#7 padding módot alkalmazva.
import numpy as np
from numpy.linalg import inv, det

def generate_key_matrix(size):
    while True:
        key = np.random.randint(0, 256, (size, size), dtype=np.int32)
        if np.gcd(int(round(det(key))) % 256, 256) == 1:
            return key

def encrypt_decrypt(input_file, output_file, key, block_size, encrypt=True):
    with open(input_file, 'rb') as f:
        data = f.read()

    result = bytearray()
    if encrypt:
        # Add PKCS#7 padding
        pad_len = block_size - (len(data) % block_size)
        if pad_len == block_size:
            pad_len = 0
        data = data + bytes([pad_len] * pad_len)
        matrix = key
    else:
        # Calculate inverse matrix for decryption
        d = int(round(det(key))) % 256
        d_inv = pow(d, -1, 256)
        matrix = (np.round(inv(key) * det(key)).astype(np.int32) % 256 * d_inv) % 256

    # Process blocks
    for i in range(0, len(data), block_size):
        block = np.array([b for b in data[i:i+block_size]], dtype=np.int32)
        processed = np.dot(matrix, block) % 256
        result.extend(processed.astype(np.uint8))

    # Remove padding if decrypting
    if not encrypt:
        pad_len = result[-1]
        result = result[:-pad_len]

    with open(output_file, 'wb') as f:
        f.write(result)

if __name__ == "__main__":
    block_size = 4
    key = generate_key_matrix(block_size)
    encrypt_decrypt("cryptHill", "encryptedHill.jpg", key, block_size, encrypt=True)
    encrypt_decrypt("encryptedHill.jpg", "decryptedHill.jpg", key, block_size, encrypt=False)
