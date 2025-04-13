import struct
import os

def tea_decrypt(v, k):
    v0, v1 = v
    k0, k1, k2, k3 = k
    delta = 0x9e3779b9
    sum = (delta * 32) & 0xFFFFFFFF
    
    for i in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF
    
    return v0, v1

def tea_encrypt(v, k):
    v0, v1 = v
    k0, k1, k2, k3 = k
    delta = 0x9e3779b9
    sum = 0
    
    for i in range(32):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    
    return v0, v1

def process_file(input_file, output_file, key, mode='decrypt'):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Keep first 80 bytes unchanged
    header = data[:80]
    data = data[80:]
    
    # Process in 8-byte blocks
    blocks = [data[i:i+8] for i in range(0, len(data), 8)]
    processed_blocks = []
    
    if mode == 'decrypt':
        for block in blocks:
            if len(block) < 8:
                processed_blocks.append(block)
                continue
            v0, v1 = struct.unpack('>II', block)
            v0, v1 = tea_decrypt((v0, v1), key)
            processed_blocks.append(struct.pack('>II', v0, v1))
    else:  # CBC encrypt
        iv = (0x00000000, 0x00000000)  # Initialization vector
        prev_block = iv
        for block in blocks:
            if len(block) < 8:
                processed_blocks.append(block)
                continue
            v0, v1 = struct.unpack('>II', block)
            # XOR with previous ciphertext
            v0 ^= prev_block[0]
            v1 ^= prev_block[1]
            v0, v1 = tea_encrypt((v0, v1), key)
            processed_blocks.append(struct.pack('>II', v0, v1))
            prev_block = (v0, v1)
    
    with open(output_file, 'wb') as f:
        f.write(header)
        f.write(b''.join(processed_blocks))

# Key: 0x0123, 0x4567, 0x89ab, 0xcdef
key = (0x0123, 0x4567, 0x89ab, 0xcdef)

# First decrypt the file
process_file('crypt.bmp', 'decrypted.bmp', key, 'decrypt')

# Then encrypt in CBC mode
process_file('decrypted.bmp', 'encrypted_cbc.bmp', key, 'encrypt')
