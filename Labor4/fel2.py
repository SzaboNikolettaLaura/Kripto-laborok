import os

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def decrypt_otp(encrypted_file, known_encrypted, known_plain):
    with open(encrypted_file, 'rb') as f:
        encrypted = f.read()
    
    with open(known_encrypted, 'rb') as f:
        known_enc = f.read()
    
    with open(known_plain, 'rb') as f:
        known_plain = f.read()
    
    # Get the key by XORing known plaintext with known ciphertext
    key = xor_bytes(known_plain, known_enc)
    
    # Decrypt the target file using the key
    decrypted = xor_bytes(encrypted, key)
    
    # Save the decrypted content
    output_file = os.path.splitext(encrypted_file)[0] + '_decrypted.docx'
    with open(output_file, 'wb') as f:
        f.write(decrypted)
    
    return output_file

if __name__ == '__main__':
    encrypted_file = 'cryptHB (2)'  # The encrypted docx file
    known_encrypted = 'cryptOTP_Massag (1)'  # The encrypted jpg
    known_plain = 'OTP_Massag (1).jpg'  # The original jpg
    
    decrypted_file = decrypt_otp(encrypted_file, known_encrypted, known_plain)
    print(f"Decrypted file saved as: {decrypted_file}")
