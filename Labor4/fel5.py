def xor_32bit(a, b):
    return a ^ b

def derive_keystream(pt_pairs, ct_pairs):
    return [xor_32bit(a, b) for a, b in zip(pt_pairs, ct_pairs)]

def decrypt_lfsr(ct, keystream):
    plaintext = bytearray()
    keystream_bytes = b''.join(k.to_bytes(4, 'big') for k in keystream)
    keystream_length = len(keystream_bytes)

    for i in range(len(ct)):
        plaintext.append(xor_32bit(ct[i], keystream_bytes[i % keystream_length]))

    return bytes(plaintext)

def main():
    pt_pairs = [0xe0ffd8ff, 0x464a1000]    
    ct_pairs = [0x880006b0, 0xde683e80]

    keystream = derive_keystream(pt_pairs, ct_pairs)

    encrypted_file = 'cryptLFSR'
    decrypted_file = 'decrypted.jpg'

    with open(encrypted_file, 'rb') as f:
        ct = f.read()

    plaintext = decrypt_lfsr(ct, keystream)

    with open(decrypted_file, 'wb') as f:
        f.write(plaintext)

if __name__ == '__main__':
    main()
