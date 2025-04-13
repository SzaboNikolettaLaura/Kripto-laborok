#7. A bmp kép Affin-256 módszerrel volt rejtjelezve, ahol a titkosítást a bájtok felett végeztük. Határozzuk meg rejtjelezéshez használt kulcsot, illetve az eredeti képet tudva, hogy 0xFF rejtjele 0x30, illetve 0x00 rejtjele 0x77 (ismert nyílt szövegű támadás / known plaintext attack).
import os
import sys

def extended_gcd(a, b):
    """Extended Euclidean algorithm for finding GCD and Bézout coefficients"""
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def modinv(a, m):
    """Find modular multiplicative inverse of a mod m"""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def solve_affine_key(p1, c1, p2, c2, m):
    """
    Solve the congruence system to find affine key (a,b):
    p1 * a + b ≡ c1 (mod m)
    p2 * a + b ≡ c2 (mod m)
    """
    # Subtract the equations to eliminate b
    # (p1 - p2) * a ≡ (c1 - c2) (mod m)
    diff_p = (p1 - p2) % m
    diff_c = (c1 - c2) % m
    
    # Find modular inverse of diff_p
    diff_p_inv = modinv(diff_p, m)
    if diff_p_inv is None:
        return None, None  # If no inverse exists
    
    # Compute a
    a = (diff_c * diff_p_inv) % m
    
    # Compute b using the first equation
    b = (c1 - a * p1) % m
    
    return a, b

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
        print("Usage: python fel7.py <encrypted_bmp_file> [output_file]")
        return
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    # Use provided output file name or create default
    output_file = sys.argv[2] if len(sys.argv) > 2 else "decrypted.bmp"
    
    # Known plaintext: 0xFF maps to 0x30, 0x00 maps to 0x77
    p1, c1 = 0xFF, 0x30  # 0xFF -> 0x30
    p2, c2 = 0x00, 0x77  # 0x00 -> 0x77
    m = 256             # Modulus
    
    # Find the key
    a, b = solve_affine_key(p1, c1, p2, c2, m)
    
    if a is None or b is None:
        print("Failed to determine the key. No valid solution found.")
        return
    
    print(f"Found key: (a={a}, b={b})")
    
    # Verify the key
    print(f"Verification: {p1} -> {(a * p1 + b) % m}, expected {c1}")
    print(f"Verification: {p2} -> {(a * p2 + b) % m}, expected {c2}")
    
    # Decrypt the file
    print(f"Decrypting {input_file} with key (a={a}, b={b})...")
    
    if decrypt_file(input_file, output_file, a, b):
        print(f"Successfully decrypted to {output_file}")
    else:
        print("Decryption failed. Invalid key.")

if __name__ == "__main__":
    main() 