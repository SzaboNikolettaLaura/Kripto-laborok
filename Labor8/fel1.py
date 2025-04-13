import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Read prime and generators from file
with open(os.path.join(current_dir, 'generatorsDH.txt'), 'r') as file:
    lines = file.readlines()
    prime = int(lines[0].strip())
    generators = [int(g.strip()) for g in lines[2:] if g.strip()]

# Function to select a generator
def select_generator():
    print(f"Found {len(generators)} generators in the file.")
    print("Which generator would you like to use?")
    print(f"Enter a number between 1 and {len(generators)}:")
    
    while True:
        try:
            choice = int(input("Your choice: "))
            if 1 <= choice <= len(generators):
                return generators[choice-1]
            else:
                print(f"Please enter a number between 1 and {len(generators)}.")
        except ValueError:
            print("Please enter a valid number.")

# Simulate Diffie-Hellman key exchange
def diffie_hellman(generator):
    # Alice generates private key and public key
    alice_private = random.randint(2, prime-2)
    alice_public = pow(generator, alice_private, prime)
    
    # Bob generates private key and public key
    bob_private = random.randint(2, prime-2)
    bob_public = pow(generator, bob_private, prime)
    
    # Exchange public keys and compute shared secret
    alice_shared_secret = pow(bob_public, alice_private, prime)
    bob_shared_secret = pow(alice_public, bob_private, prime)
    
    # Verify both parties computed the same key
    assert alice_shared_secret == bob_shared_secret, "DH key exchange failed"
    
    # Return the shared secret
    return alice_shared_secret

# Derive AES key from shared secret
def derive_key(shared_secret):
    # Convert the shared secret to bytes and hash it to get a 16-byte (128-bit) AES key
    key_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big')
    return key_bytes[:16]  # Use first 16 bytes for AES-128

# Encrypt file using AES
def encrypt_file(input_path, output_path, key):
    # Generate a random IV
    iv = os.urandom(16)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        # Read the file content
        plaintext = infile.read()
        
        # Pad the plaintext to be a multiple of 16 bytes
        padded_plaintext = pad(plaintext, AES.block_size)
        
        # Encrypt the padded plaintext
        ciphertext = cipher.encrypt(padded_plaintext)
        
        # Write IV and ciphertext to the output file
        outfile.write(iv + ciphertext)

# Decrypt file using AES
def decrypt_file(input_path, output_path, key):
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        # Read IV and ciphertext
        iv = infile.read(16)
        ciphertext = infile.read()
        
        # Create AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt the ciphertext and remove padding
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        # Write decrypted data to output file
        outfile.write(decrypted_data)

# Main function
def main():
    print("Diffie-Hellman Key Exchange and AES Encryption/Decryption")
    print(f"Using prime from file: {prime}")
    
    # Let user select a generator
    generator = select_generator()
    print(f"Using generator: {generator}")
    
    # Perform Diffie-Hellman key exchange
    shared_secret = diffie_hellman(generator)
    print(f"Shared secret: {shared_secret}")
    
    # Derive AES key from shared secret
    aes_key = derive_key(shared_secret)
    print(f"AES key (first 16 bytes): {aes_key.hex()}")
    
    # Input/output file paths for encryption
    input_file = input("Enter the path of the file to encrypt: ")
    encrypted_file = input("Enter the path for the encrypted output: ")
    
    # Encrypt the file
    encrypt_file(input_file, encrypted_file, aes_key)
    print(f"File encrypted and saved to {encrypted_file}")
    
    # Input/output file paths for decryption
    decrypted_file = input("Enter the path for the decrypted output: ")
    
    # Decrypt the file
    decrypt_file(encrypted_file, decrypted_file, aes_key)
    print(f"File decrypted and saved to {decrypted_file}")

if __name__ == "__main__":
    main()
