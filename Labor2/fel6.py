#6. A jpg kép Affin-256 módszerrel volt rejtjelezve, ahol a titkosítást a bájtok felett végeztük. Határozzuk meg az eredeti képet tudva, hogy a rejtjelezéshez használt kulcs (a, b) = (113, 223).
import os
import sys

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

def main():
    if len(sys.argv) < 2:
        print("Usage: python fel6.py <encrypted_jpg_file> [output_file]")
        return
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    # Use provided output file name or create default
    output_file = sys.argv[2] if len(sys.argv) > 2 else "decrypted.jpg"
    
    # Known key (a, b) = (113, 223)
    a, b = 113, 223
    
    print(f"Decrypting {input_file} with key (a={a}, b={b})...")
    
    if decrypt_file(input_file, output_file, a, b):
        print(f"Successfully decrypted to {output_file}")
    else:
        print("Decryption failed. Invalid key.")

if __name__ == "__main__":
    main() 