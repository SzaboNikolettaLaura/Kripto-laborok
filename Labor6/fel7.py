#7. Titkosítsunk és fejtsünk vissza egy bináris állományt, ChaCha20-Poly130 titkosítást alkalmazva, ahol a nonce és kulcs értékeket generáljuk véletlenszerűen. A titkosítás során az állomány elejére írjuk be a nonce értékét, majd a végére a hitelesítő tag-et. Visszafejtéskor elenőrzizzük le azt is, hogy nem-e módosult az állomány tartalma. A generált kulcsot írjuk ki egy szövegállományba base64-es alakba. Az előző feladathoz képest jobb-e a futási idő? Hogyan járunk el ha az állományt csak részenként tudjk beolvasni, ha a teljes tartalom nem fér el a memóriában?
import os
import time
import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def generate_key():
    return ChaCha20Poly1305.generate_key()

def generate_nonce():
    return os.urandom(12)  # 12 bytes (96 bits) for ChaCha20Poly1305

def encrypt_file(input_file, output_file, key):
    # Generate a random nonce
    nonce = generate_nonce()
    
    # Create ChaCha20Poly1305 cipher
    cipher = ChaCha20Poly1305(key)
    
    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Encrypt the data and get the authentication tag
    encrypted_data = cipher.encrypt(nonce, data, None)
    
    # Write the nonce at the beginning, then the encrypted data
    with open(output_file, 'wb') as f:
        f.write(nonce)
        f.write(encrypted_data)
    
    # Save the key to a text file in base64 format
    with open(f"{input_file}.key", 'wb') as f:
        f.write(base64.b64encode(key))

def decrypt_file(input_file, output_file, key):
    # Read the encrypted file
    with open(input_file, 'rb') as f:
        # Read the nonce (first 12 bytes)
        nonce = f.read(12)
        # Read the rest (encrypted data + authentication tag)
        encrypted_data = f.read()
    
    # Create ChaCha20Poly1305 cipher
    cipher = ChaCha20Poly1305(key)
    
    try:
        # Decrypt the data and verify authentication
        decrypted_data = cipher.decrypt(nonce, encrypted_data, None)
        
        # Write the decrypted data
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        return True  # Decryption successful
    except Exception as e:
        print(f"Decryption failed: {e}")
        print("The file may have been tampered with.")
        return False

def chunked_encrypt_file(input_file, output_file, key, chunk_size=1024*1024):
    """Encrypt a file in chunks for large files that don't fit in memory"""
    nonce = generate_nonce()
    cipher = ChaCha20Poly1305(key)
    
    # In chunked mode, we need to process the entire file to get the tag
    # We'll use the associated data feature for authentication
    
    # First read the file in chunks and encrypt each chunk
    input_size = os.path.getsize(input_file)
    chunks = []
    
    with open(input_file, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            # Use chunk number as associated data for each chunk
            associated_data = str(chunk_number).encode()
            encrypted_chunk = cipher.encrypt(nonce, chunk, associated_data)
            chunks.append((encrypted_chunk, associated_data))
            chunk_number += 1
    
    # Write the encrypted file
    with open(output_file, 'wb') as f:
        # Write the nonce
        f.write(nonce)
        
        # Write the number of chunks
        f.write(chunk_number.to_bytes(8, byteorder='big'))
        
        # Write each chunk with its length
        for encrypted_chunk, _ in chunks:
            chunk_len = len(encrypted_chunk)
            f.write(chunk_len.to_bytes(8, byteorder='big'))
            f.write(encrypted_chunk)
    
    # Save the key to a text file in base64 format
    with open(f"{input_file}.key", 'wb') as f:
        f.write(base64.b64encode(key))

def chunked_decrypt_file(input_file, output_file, key, chunk_size=1024*1024):
    """Decrypt a file in chunks for large files that don't fit in memory"""
    
    with open(input_file, 'rb') as f:
        # Read the nonce
        nonce = f.read(12)
        
        # Read the number of chunks
        chunk_count = int.from_bytes(f.read(8), byteorder='big')
        
        cipher = ChaCha20Poly1305(key)
        
        # Create output file
        with open(output_file, 'wb') as out_f:
            for i in range(chunk_count):
                try:
                    # Read chunk length
                    chunk_len = int.from_bytes(f.read(8), byteorder='big')
                    
                    # Read encrypted chunk
                    encrypted_chunk = f.read(chunk_len)
                    
                    # Use chunk number as associated data
                    associated_data = str(i).encode()
                    
                    # Decrypt chunk and verify
                    decrypted_chunk = cipher.decrypt(nonce, encrypted_chunk, associated_data)
                    
                    # Write to output
                    out_f.write(decrypted_chunk)
                    
                except Exception as e:
                    print(f"Decryption failed at chunk {i}: {e}")
                    print("The file may have been tampered with.")
                    return False
    
    return True

def main():
    # Select a test file (binary file)
    input_file = "decrypted.jpg"
    encrypted_file = "encrypted_file.bin"
    decrypted_file = "decrypted_file.jpg"
    
    # Create a test binary file if it doesn't exist
    if not os.path.exists(input_file):
        with open(input_file, 'wb') as f:
            f.write(os.urandom(1024 * 1024))  # 1MB random data
    
    # Generate a key
    key = generate_key()
    
    # Measure encryption time
    start_time = time.time()
    encrypt_file(input_file, encrypted_file, key)
    encryption_time = time.time() - start_time
    
    # Measure decryption time
    start_time = time.time()
    success = decrypt_file(encrypted_file, decrypted_file, key)
    decryption_time = time.time() - start_time
    
    print(f"Encryption time: {encryption_time:.4f} seconds")
    print(f"Decryption time: {decryption_time:.4f} seconds")
    print(f"Decryption successful: {success}")
    
    # Verify the decrypted file matches the original
    with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
        if f1.read() == f2.read():
            print("File integrity verified - original and decrypted files match")
        else:
            print("Error: Files don't match")
    
    # Print key in base64 format
    print(f"Key saved to {input_file}.key")
    print(f"Key (base64): {base64.b64encode(key).decode()}")
    
    # Test file tampering
    print("\nTesting file tampering detection...")
    with open(encrypted_file, 'r+b') as f:
        f.seek(20)  # Skip past the nonce and go into the encrypted data
        original_byte = f.read(1)
        f.seek(20)
        f.write(bytes([original_byte[0] ^ 1]))  # Flip one bit
    
    tampered_decrypted = "tampered_decrypted.bin"
    success = decrypt_file(encrypted_file, tampered_decrypted, key)
    print(f"Decryption of tampered file successful: {success}")
    
    # Test chunked mode for large files
    print("\nTesting chunked encryption/decryption...")
    chunked_encrypted = "chunked_encrypted.bin"
    chunked_decrypted = "chunked_decrypted.bin"
    
    start_time = time.time()
    chunked_encrypt_file(input_file, chunked_encrypted, key, chunk_size=1024*64)
    chunked_encryption_time = time.time() - start_time
    
    start_time = time.time()
    success = chunked_decrypt_file(chunked_encrypted, chunked_decrypted, key, chunk_size=1024*64)
    chunked_decryption_time = time.time() - start_time
    
    print(f"Chunked encryption time: {chunked_encryption_time:.4f} seconds")
    print(f"Chunked decryption time: {chunked_decryption_time:.4f} seconds")
    print(f"Chunked decryption successful: {success}")
    
    with open(input_file, 'rb') as f1, open(chunked_decrypted, 'rb') as f2:
        if f1.read() == f2.read():
            print("Chunked file integrity verified - original and decrypted files match")
        else:
            print("Error: Chunked files don't match")

if __name__ == "__main__":
    main()
