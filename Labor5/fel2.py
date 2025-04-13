#2. Titkosítsunk és fejtsünk vissza egy tetszőleges bináris állományt, rendre DES3-CBC, DES3-CTR, AES-CBC, AES-CTR módban, használva az általunk kiválasztott programozási nyelvhez megírt crypto könyvtárcsomagot. Forráskódok: bináris állomány titkosítása, visszafejtése a Blowfish-CBC algoritmussal Python, OpenSSL, Crypto++, Java.
from Crypto.Cipher import DES3, AES
from Crypto.Random import get_random_bytes
import os

CHUNK_SIZE = 1024  # 1KB chunks

def encrypt_file(input_file, output_file, cipher_type, mode, key, iv=None, nonce=None):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        if cipher_type == 'DES3':
            if mode == DES3.MODE_CTR:
                cipher = DES3.new(key, mode, nonce=nonce)
            else:
                cipher = DES3.new(key, mode, iv=iv)
        else:  # AES
            if mode == AES.MODE_CTR:
                cipher = AES.new(key, mode, nonce=nonce)
            else:
                cipher = AES.new(key, mode, iv=iv)
        
        while True:
            chunk = f_in.read(CHUNK_SIZE)
            if not chunk:
                break
            encrypted_chunk = cipher.encrypt(chunk)
            f_out.write(encrypted_chunk)

def decrypt_file(input_file, output_file, cipher_type, mode, key, iv=None, nonce=None):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        if cipher_type == 'DES3':
            if mode == DES3.MODE_CTR:
                cipher = DES3.new(key, mode, nonce=nonce)
            else:
                cipher = DES3.new(key, mode, iv=iv)
        else:  # AES
            if mode == AES.MODE_CTR:
                cipher = AES.new(key, mode, nonce=nonce)
            else:
                cipher = AES.new(key, mode, iv=iv)
        
        while True:
            chunk = f_in.read(CHUNK_SIZE)
            if not chunk:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            f_out.write(decrypted_chunk)

# Test the functions
input_file = "decrypted.bmp"
output_enc = "encrypted.bmp"
output_dec = "decrypted.bmp"

# Generate random keys and IVs
des3_key = get_random_bytes(24)  # 24 bytes for DES3
aes_key = get_random_bytes(32)   # 32 bytes for AES-256
des3_iv = get_random_bytes(8)    # 8 bytes IV for DES3
aes_iv = get_random_bytes(16)    # 16 bytes IV for AES
des3_nonce = get_random_bytes(2) # 7 bytes nonce for DES3 CTR
aes_nonce = get_random_bytes(2)  # 8 bytes nonce for AES CTR

# Test DES3-CBC
encrypt_file(input_file, output_enc, 'DES3', DES3.MODE_CBC, des3_key, des3_iv)
decrypt_file(output_enc, output_dec, 'DES3', DES3.MODE_CBC, des3_key, des3_iv)

# Test DES3-CTR
encrypt_file(input_file, output_enc, 'DES3', DES3.MODE_CTR, des3_key, nonce=des3_nonce)
decrypt_file(output_enc, output_dec, 'DES3', DES3.MODE_CTR, des3_key, nonce=des3_nonce)

# Test AES-CBC
encrypt_file(input_file, output_enc, 'AES', AES.MODE_CBC, aes_key, aes_iv)
decrypt_file(output_enc, output_dec, 'AES', AES.MODE_CBC, aes_key, aes_iv)

# Test AES-CTR
encrypt_file(input_file, output_enc, 'AES', AES.MODE_CTR, aes_key, nonce=aes_nonce)
decrypt_file(output_enc, output_dec, 'AES', AES.MODE_CTR, aes_key, nonce=aes_nonce)        