#5. Egy jpg kép Affin-256 módszerrel volt rejtjelezve, ahol a titkosítást a bájtok felett végeztük. Határozzuk meg az eredeti képet és a rejtjelezéshez használt kulcsot az összes kulcs kipróbálásának módszerével, tudva azt, hogy egy jpg első két bájtja 0xFF, 0xD8.
import os
import sys
from math import gcd

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def decrypt_byte(c, a, b, m=256):
    """Decrypt a single byte using affine cipher"""
    a_inv = modinv(a, m)
    if a_inv is None:
        return None
    return (a_inv * (c - b)) % m

def decrypt_file(input_file, output_file, a, b):
    """Decrypt file encrypted with Affine-256 cipher"""
    with open(input_file, 'rb') as f:
        data = f.read()
    
    decrypted = bytearray()
    for byte in data:
        dec_byte = decrypt_byte(byte, a, b)
        if dec_byte is None:
            return False  # Invalid key
        decrypted.append(dec_byte)
    
    with open(output_file, 'wb') as f:
        f.write(decrypted)
    
    return True

def is_valid_jpg(first_two_bytes):
    """Check if the first two bytes match the JPG signature"""
    return first_two_bytes[0] == 0xFF and first_two_bytes[1] == 0xD8

def brute_force_affine256(input_file):
    """Try all possible valid keys for Affine-256 and check for JPG signature"""
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    if len(encrypted_data) < 2:
        print("Input file too small")
        return None
    
    # First two bytes of the encrypted file
    c1, c2 = encrypted_data[0], encrypted_data[1]
    
    # Known plaintext: first two bytes of a JPG file
    p1, p2 = 0xFF, 0xD8
    
    # Modulus
    m = 256
    
    valid_keys = []
    
    # Try all possible values of 'a' (must be coprime with 256)
    for a in range(1, m):
        if gcd(a, m) == 1:  # Check if 'a' is coprime with 256
            a_inv = modinv(a, m)
            
            # Try to deduce 'b' using the first known plaintext
            b = (c1 - a * p1) % m
            
            # Check if this key correctly decrypts the second byte
            if (a * p2 + b) % m == c2:
                valid_keys.append((a, b))
    
    return valid_keys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fel5.py <encrypted_jpg_file>")
        return
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    print(f"Searching for valid Affine-256 keys for {input_file}...")
    valid_keys = brute_force_affine256(input_file)
    
    if not valid_keys:
        print("No valid keys found.")
        return
    
    print(f"Found {len(valid_keys)} potential keys: {valid_keys}")
    
    # Try each key and save the decrypted file
    for i, (a, b) in enumerate(valid_keys):
        output_file = f"decrypted_{i+1}.jpg"
        print(f"Trying key (a={a}, b={b}) -> {output_file}")
        
        if decrypt_file(input_file, output_file, a, b):
            print(f"Successfully decrypted with key (a={a}, b={b}) to {output_file}")
        else:
            print(f"Failed to decrypt with key (a={a}, b={b})")

if __name__ == "__main__":
    main() 