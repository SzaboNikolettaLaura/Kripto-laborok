import os
import struct
import random
import sys

def generate_key():
    return [random.getrandbits(32) for _ in range(4)]

def tea_encrypt(block, key):
    v0, v1 = struct.unpack('>2I', block)
    delta = 0x9e3779b9
    sum_val = 0
    for _ in range(32):
        sum_val = (sum_val + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + key[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + key[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + key[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + key[3]))) & 0xFFFFFFFF
    return struct.pack('>2I', v0, v1)

def tea_decrypt(block, key):
    v0, v1 = struct.unpack('>2I', block)
    delta = 0x9e3779b9
    sum_val = (delta * 32) & 0xFFFFFFFF
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + key[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + key[1]))) & 0xFFFFFFFF
        sum_val = (sum_val - delta) & 0xFFFFFFFF
    return struct.pack('>2I', v0, v1)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad_data(data):
    padding_length = 8 - (len(data) % 8)
    return data + bytes([padding_length] * padding_length)

def unpad_data(data):
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_file(input_file, output_file, mode='CBC'):
    key = generate_key()
    iv = os.urandom(8)
    with open(input_file, 'rb') as f:
        data = f.read()
    padded_data = pad_data(data)
    encrypted_data = b''
    if mode == 'CBC':
        prev_block = iv
        for i in range(0, len(padded_data), 8):
            block = padded_data[i:i+8]
            xored_block = xor_bytes(block, prev_block)
            encrypted_block = tea_encrypt(xored_block, key)
            encrypted_data += encrypted_block
            prev_block = encrypted_block
    elif mode == 'CTR':
        counter = 0
        for i in range(0, len(padded_data), 8):
            block = padded_data[i:i+8]
            counter_block = struct.pack('>Q', counter)
            encrypted_counter = tea_encrypt(counter_block, key)
            encrypted_block = xor_bytes(block, encrypted_counter)
            encrypted_data += encrypted_block
            counter += 1
    with open(output_file, 'wb') as f:
        f.write(struct.pack('>I', len(key)))
        for k in key:
            f.write(struct.pack('>I', k))
        f.write(iv)
        f.write(encrypted_data)

def decrypt_file(input_file, output_file, mode='CBC'):
    with open(input_file, 'rb') as f:
        key_length = struct.unpack('>I', f.read(4))[0]
        key = [struct.unpack('>I', f.read(4))[0] for _ in range(key_length)]
        iv = f.read(8)
        encrypted_data = f.read()
    decrypted_data = b''
    if mode == 'CBC':
        prev_block = iv
        for i in range(0, len(encrypted_data), 8):
            block = encrypted_data[i:i+8]
            decrypted_block = tea_decrypt(block, key)
            xored_block = xor_bytes(decrypted_block, prev_block)
            decrypted_data += xored_block
            prev_block = block
    elif mode == 'CTR':
        counter = 0
        for i in range(0, len(encrypted_data), 8):
            block = encrypted_data[i:i+8]
            counter_block = struct.pack('>Q', counter)
            encrypted_counter = tea_encrypt(counter_block, key)
            decrypted_block = xor_bytes(block, encrypted_counter)
            decrypted_data += decrypted_block
            counter += 1
    unpadded_data = unpad_data(decrypted_data)
    with open(output_file, 'wb') as f:
        f.write(unpadded_data)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python fel3.py <encrypt/decrypt> <input_file> <output_file> <CBC/CTR>')
        sys.exit(1)
    mode = sys.argv[4].upper()
    if sys.argv[1] == 'encrypt':
        encrypt_file(sys.argv[2], sys.argv[3], mode)
    elif sys.argv[1] == 'decrypt':
        decrypt_file(sys.argv[2], sys.argv[3], mode)
