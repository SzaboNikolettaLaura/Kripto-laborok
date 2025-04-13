#4. Egy jpg állomány CBC blokk-titkosító módszert alkalmazva, affine, mod 256 titkosítóval volt titkosítva. Határozzuk meg az eredeti jpg állományt, a jpg titkosított értéke alapján, tudva, hogy az IV értéke (19), a titkosító kulcs pedig (157, 45).
import numpy as np
from PIL import Image

def affine_decrypt(c, a, b):
    a_inv = pow(a, -1, 256)
    return (a_inv * (c - b)) % 256

def cbc_decrypt(encrypted_data, a, b, iv):
    decrypted = bytearray()
    prev_block = iv
    
    for i in range(0, len(encrypted_data)):
        current_block = encrypted_data[i]
        decrypted_byte = affine_decrypt(current_block, a, b)
        plain_byte = decrypted_byte ^ prev_block
        decrypted.append(plain_byte)
        prev_block = current_block
    
    return bytes(decrypted)

def decrypt_image(input_path, output_path, a, b, iv):
    with open(input_path, 'rb') as f:
        encrypted_data = f.read()
    
    decrypted_data = cbc_decrypt(encrypted_data, a, b, iv)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

# Parameters
a = 157
b = 45
iv = 19

# Decrypt the image
decrypt_image('cryptAffine256_Tanacs', 'decrypted.jpg', a, b, iv)
