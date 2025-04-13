#3. Határozzuk meg azt a nyílt szöveget, amelyről tudjuk, hogy három különböző félnek RSA-textbookkal rejtjelezve volt elküldve, ahol a következő linken elérhetőek a felek nyilvános kulcsai, illetve a rejtjelezett szövegek:
import math
import decimal
from functools import reduce

def read_key_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().strip()
        # Assuming the file contains only the n value
        n = int(content)
        # For this attack, we know e is 3
        e = 3
    return n, e

def read_crypt_file(filename):
    with open(filename, 'rb') as f:
        content = f.read()
        # Try to convert from binary to int
        return int.from_bytes(content, byteorder='big')

def chinese_remainder_theorem(congruences):
    # Step 1: Calculate the product of all moduli
    moduli = [congruence[1] for congruence in congruences]
    N = reduce(lambda x, y: x * y, moduli)
    
    result = 0
    for a_i, n_i in congruences:
        # Step 2: Calculate N_i = N / n_i
        N_i = N // n_i
        
        # Step 3: Calculate the modular multiplicative inverse of N_i modulo n_i
        inv = pow(N_i, -1, n_i)
        
        # Step 4: Add to the result
        result += a_i * N_i * inv
    
    # Step 5: Return the result modulo N
    return result % N

def main():
    # Read the keys and ciphertexts
    n1, e1 = read_key_file("key200_1.txt")
    n2, e2 = read_key_file("key200_2.txt")
    n3, e3 = read_key_file("key200_3.txt")
    
    c1 = read_crypt_file("cryptE3_1")
    c2 = read_crypt_file("cryptE3_2")
    c3 = read_crypt_file("cryptE3_3")
    
    # Check that all exponents are 3 (required for this attack)
    if e1 != 3 or e2 != 3 or e3 != 3:
        print("This attack requires all exponents to be 3")
        return
    
    # Apply Chinese Remainder Theorem
    congruences = [(c1, n1), (c2, n2), (c3, n3)]
    x = chinese_remainder_theorem(congruences)
    
    # Find the cube root
    decimal.getcontext().prec = 100
    nr = math.ceil(pow(x, 1/decimal.Decimal(3)))
    
    # Convert to bytes and decode
    try:
        plaintext_bytes = nr.to_bytes((nr.bit_length() + 7) // 8, 'big')
        plaintext = plaintext_bytes.decode('utf-8')
        print(f"Recovered plaintext: {plaintext}")
    except Exception as e:
        print(f"Error decoding plaintext: {e}")
        print(f"Numeric value: {nr}")

if __name__ == "__main__":
    main()
