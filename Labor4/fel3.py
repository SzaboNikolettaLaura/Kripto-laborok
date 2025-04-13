def decrypt_otp(encrypted_file, output_file):
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Known plaintext: <!DOCTYPE html>\n
    known_plaintext = b'<!DOCTYPE html>\n'
    
    # Get first 16 bytes of encrypted data
    first_16_bytes = encrypted_data[:16]
    
    # Calculate key by XORing known plaintext with encrypted data
    key = bytes([a ^ b for a, b in zip(first_16_bytes, known_plaintext)])
    
    # Decrypt the entire file
    decrypted_data = bytearray()
    for i, byte in enumerate(encrypted_data):
        decrypted_data.append(byte ^ key[i % 16])
    
    # Write decrypted data to output file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    encrypted_file = "cryptOTP"  # Replace with your encrypted file name
    output_file = "decrypted.html"
    decrypt_otp(encrypted_file, output_file)
