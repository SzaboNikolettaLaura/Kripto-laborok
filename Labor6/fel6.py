import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key():
    return AESGCM.generate_key(bit_length=256)

def generate_nonce():
    return os.urandom(12)  # 96 bits is recommended for GCM

def encrypt_file(input_file, output_file, key_file):
    # Generate random key and nonce
    key = generate_key()
    nonce = generate_nonce()
    
    # Save key to file in base64 format
    with open(key_file, 'wb') as f:
        f.write(base64.b64encode(key))
    
    # Initialize AESGCM with the key
    aesgcm = AESGCM(key)
    
    # Process file in chunks (for large files)
    chunk_size = 1024 * 1024  # 1MB chunks
    
    with open(input_file, 'rb') as in_file:
        # Read entire file content
        data = in_file.read()
    
    # Encrypt data
    ciphertext = aesgcm.encrypt(nonce, data, None)
    
    # Write to output file: nonce + ciphertext + tag (tag is included in ciphertext from cryptography library)
    with open(output_file, 'wb') as out_file:
        out_file.write(nonce)
        out_file.write(ciphertext)

def encrypt_large_file(input_file, output_file, key_file):
    # Generate random key and nonce
    key = generate_key()
    nonce = generate_nonce()
    
    # Save key to file in base64 format
    with open(key_file, 'wb') as f:
        f.write(base64.b64encode(key))
    
    # Initialize AESGCM with the key
    aesgcm = AESGCM(key)
    
    # For large files, we need to use a different approach
    # Read the file in chunks, concatenate, then encrypt
    # This is because GCM requires the entire message for authentication
    
    # First, get file size
    file_size = os.path.getsize(input_file)
    
    # Buffer for the whole file data (not ideal for very large files)
    # For truly huge files, we would need streaming AEAD which GCM doesn't support directly
    all_data = bytearray()
    
    # Read input file in chunks
    with open(input_file, 'rb') as in_file:
        chunk = in_file.read(1024 * 1024)  # 1MB chunks
        while chunk:
            all_data.extend(chunk)
            chunk = in_file.read(1024 * 1024)
    
    # Encrypt all data at once (GCM needs the complete message)
    ciphertext = aesgcm.encrypt(nonce, all_data, None)
    
    # Write output: nonce + ciphertext
    with open(output_file, 'wb') as out_file:
        out_file.write(nonce)
        out_file.write(ciphertext)

def decrypt_file(input_file, output_file, key_file):
    # Load key from file
    with open(key_file, 'rb') as f:
        key = base64.b64decode(f.read())
    
    # Initialize AESGCM with the key
    aesgcm = AESGCM(key)
    
    with open(input_file, 'rb') as in_file:
        # Read nonce (first 12 bytes)
        nonce = in_file.read(12)
        
        # Read the rest (ciphertext + tag)
        ciphertext = in_file.read()
    
    try:
        # Decrypt and verify
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Write decrypted data to output file
        with open(output_file, 'wb') as out_file:
            out_file.write(plaintext)
        
        return True  # Authentication successful
    except Exception as e:
        print(f"Authentication or decryption failed: {e}")
        return False  # Authentication failed

def decrypt_large_file(input_file, output_file, key_file):
    # Similar to decrypt_file but reads the ciphertext in chunks
    # Load key from file
    with open(key_file, 'rb') as f:
        key = base64.b64decode(f.read())
    
    # Initialize AESGCM with the key
    aesgcm = AESGCM(key)
    
    # First read the nonce
    with open(input_file, 'rb') as in_file:
        nonce = in_file.read(12)
        
        # Read the rest (ciphertext) in chunks
        ciphertext = bytearray()
        chunk = in_file.read(1024 * 1024)  # 1MB chunks
        while chunk:
            ciphertext.extend(chunk)
            chunk = in_file.read(1024 * 1024)
    
    try:
        # Decrypt and verify
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Write decrypted data to output file
        with open(output_file, 'wb') as out_file:
            out_file.write(plaintext)
        
        return True  # Authentication successful
    except Exception as e:
        print(f"Authentication or decryption failed: {e}")
        return False  # Authentication failed

if __name__ == "__main__":
    # Example usage
    input_file = "decrypted.jpg"
    encrypted_file = "encrypted.bin"
    decrypted_file = "decrypted_6.jpg"
    key_file = "key.txt"
    
    # Check if the file is large (e.g., > 100MB)
    if os.path.exists(input_file) and os.path.getsize(input_file) > 100 * 1024 * 1024:
        encrypt_large_file(input_file, encrypted_file, key_file)
        success = decrypt_large_file(encrypted_file, decrypted_file, key_file)
    else:
        encrypt_file(input_file, encrypted_file, key_file)
        success = decrypt_file(encrypted_file, decrypted_file, key_file)
    
    if success:
        print("File encrypted and decrypted successfully with authentication verified.")
    else:
        print("Decryption failed due to authentication error - file may have been tampered with.")
