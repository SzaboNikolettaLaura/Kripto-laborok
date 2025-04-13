import math
import random
import sympy as sp
import sys
import os

def keyGen(n, MOD):
    while True:
        key = sp.Matrix([[random.randint(0, MOD-1) for i in range(n)]for j in range(n)])
        det = key.det() % MOD
        if math.gcd(det, MOD) != 1:
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            key[i, j] = random.randint(0,MOD-1)
        else: break
    
    keyInv = key.inv_mod(MOD)
    return key, keyInv

def text_to_matrix(text, n, MOD):
    # Pad the text if necessary
    if len(text) % n != 0:
        text += ' ' * (n - len(text) % n)
    
    # Convert text to matrix
    blocks = []
    for i in range(0, len(text), n):
        block = sp.Matrix([[ord(text[i+j]) % MOD] for j in range(n)])
        blocks.append(block)
    
    return blocks

def matrix_to_text(matrices, MOD):
    text = ""
    for matrix in matrices:
        for i in range(matrix.rows):
            text += chr(int(matrix[i, 0]) % MOD)
    
    return text

def encrypt_file(input_file, output_file, key, n, MOD):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Convert text to matrix blocks
        blocks = text_to_matrix(text, n, MOD)
        
        # Encrypt each block
        encrypted_blocks = []
        for block in blocks:
            encrypted_block = (key * block) % MOD
            encrypted_blocks.append(encrypted_block)
        
        # Save encrypted data
        with open(output_file, 'w', encoding='utf-8') as f:
            for block in encrypted_blocks:
                for i in range(block.rows):
                    f.write(chr(int(block[i, 0])))
        
        print(f"File encrypted successfully: {output_file}")
    
    except Exception as e:
        print(f"Error encrypting file: {e}")

def decrypt_file(input_file, output_file, key_inv, n, MOD):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Convert encrypted text to matrix blocks
        blocks = text_to_matrix(text, n, MOD)
        
        # Decrypt each block
        decrypted_blocks = []
        for block in blocks:
            decrypted_block = (key_inv * block) % MOD
            decrypted_blocks.append(decrypted_block)
        
        # Save decrypted data
        with open(output_file, 'w', encoding='utf-8') as f:
            decrypted_text = matrix_to_text(decrypted_blocks, MOD)
            f.write(decrypted_text)
        
        print(f"File decrypted successfully: {output_file}")
    
    except Exception as e:
        print(f"Error decrypting file: {e}")

def main():
    # Parameters
    n = 3      # Matrix size
    MOD = 256  # Use 256 for ASCII encoding
    
    # Generate key
    key, key_inv = keyGen(n, MOD)
    print("Key generated successfully")
    
    # Menu
    while True:
        print("\nHill Cipher Menu:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path: ")
            encrypt_file(input_file, output_file, key, n, MOD)
        
        elif choice == '2':
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path: ")
            decrypt_file(input_file, output_file, key_inv, n, MOD)
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()