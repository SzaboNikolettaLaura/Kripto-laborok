#5. Egy jpg állomány CBC blokk-titkosító módszert alkalmazva, Hill, mod 256 titkosítóval volt titkosítva. Határozzuk meg az eredeti jpg állományt, a jpg titkosított értéke alapján, ismerve a titkosító kulcsot, illetve tudva azt, hogy az IV értéke a titkosított állomány utolsó négy bájtjára van beírva
import numpy as np
from PIL import Image

def load_key(key_file):
    with open(key_file, 'r') as f:
        size = int(f.readline().strip())
        key = []
        for _ in range(size):
            row = list(map(int, f.readline().strip().split()))
            key.append(row)
        return key

def hill_decrypt(block, key):
    key_matrix = np.array(key, dtype=np.int32)
    key_inv = np.linalg.inv(key_matrix)
    det = int(round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 256)
    key_inv = (key_inv * det * det_inv) % 256
    key_inv = key_inv.astype(np.int32)
    result = np.dot(block.astype(np.int32), key_inv) % 256
    return result.astype(np.uint8)

def cbc_decrypt(encrypted_data, key, block_size=4):
    # Get IV from last block
    iv = encrypted_data[-block_size:]
    encrypted_data = encrypted_data[:-block_size]
    
    if len(encrypted_data) % block_size != 0:
        pad_length = block_size - (len(encrypted_data) % block_size)
        encrypted_data = encrypted_data + b'\x00' * pad_length
    
    decrypted_data = bytearray()
    prev_cipher = iv
    
    # Process each block
    for i in range(0, len(encrypted_data), block_size):
        current_cipher = encrypted_data[i:i+block_size]
        block = np.frombuffer(current_cipher, dtype=np.uint8)
        
        # Hill decrypt
        decrypted = hill_decrypt(block, key)
        
        # XOR with previous cipher block
        prev_block = np.frombuffer(prev_cipher, dtype=np.uint8)
        plaintext = np.bitwise_xor(decrypted, prev_block)
        
        decrypted_data.extend(plaintext)
        prev_cipher = current_cipher
    
    return bytes(decrypted_data)

def decrypt_jpg(encrypted_file, key_file, output_file):
    key = load_key(key_file)
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    
    decrypted_data = cbc_decrypt(encrypted_data, key)
    
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

# Decrypt the file
decrypt_jpg('cryptHillCBC_Ikrek', 'keyHillCBC.txt', 'decrypted_5.jpg')
