import os
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Task 2: Decrypt crypted8_2.jpg
def task2():
    # Read the DH parameters
    with open('DHKey8_2.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    
    p = int(lines[0], 16)
    q = int(lines[1], 16)
    g = int(lines[2], 16)
    
    # Read A's private key
    with open('APrivFile.txt', 'r') as f:
        a_priv = int(f.read().strip(), 16)
    
    # Read B's public key
    with open('BPubFile.txt', 'r') as f:
        b_pub = int(f.read().strip(), 16)
    
    # Calculate shared secret using DH key exchange
    shared_secret = pow(b_pub, a_priv, p)
    shared_secret_hex = hex(shared_secret)[2:]  # Remove '0x' prefix
    
    # Generate AES key using scrypt KDF
    salt = binascii.unhexlify('438bcc1fd2bb1363e90fb6ff4756bc58')
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**10,
        r=8,
        p=1,
        backend=default_backend()
    )
    aes_key = kdf.derive(binascii.unhexlify(shared_secret_hex))
    
    # Read the encrypted file
    with open('crypted8_2.jpg', 'rb') as f:
        encrypted_data = f.read()
    
    # Extract nonce (first 8 bytes) and encrypted data
    nonce = encrypted_data[:8]
    encrypted_content = encrypted_data[8:]
    
    # Create AES-CTR cipher with the nonce and initial counter value 1
    counter = 1
    ctr = nonce + counter.to_bytes(8, byteorder='big')
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(ctr), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_content) + decryptor.finalize()
    
    # Write the decrypted data to a file
    with open('decrypted8_2.jpg', 'wb') as f:
        f.write(decrypted_data)
    
    print("File decrypted successfully!")

if __name__ == "__main__":
    # Task 2: Decrypting crypted8_2.jpg
    task2()
