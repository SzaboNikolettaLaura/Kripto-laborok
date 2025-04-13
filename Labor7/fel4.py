#4. Az RSA kriptorendszer visszafejtésének időigényét gyorsítani lehet, ha alkalmazzuk a kínai maradéktételt. Alkalmazzuk ezt a gyorsítási folyamatot az RSA-textbook esetében. Írjunk programot, melyben összehasonlítjuk a két visszafejtési algoritmus időigényét.
import random
import time
from math import gcd

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    # Find d such that n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a random prime number with specified bit length"""
    while True:
        p = random.getrandbits(bits)
        # Ensure the number is odd and has the correct bit length
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p

def mod_inverse(a, m):
    """Calculate the modular multiplicative inverse of a mod m"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def generate_keys(bits):
    """Generate RSA key pair"""
    # Generate two distinct prime numbers
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    # Compute d such that (d * e) % phi = 1
    d = mod_inverse(e, phi)
    
    return (n, e), (n, d, p, q)

def rsa_encrypt(message, public_key):
    """Encrypt a message using RSA"""
    n, e = public_key
    # Ensure message is less than n
    if message >= n:
        raise ValueError("Message too large for the key size")
    return pow(message, e, n)

def rsa_decrypt_standard(ciphertext, private_key):
    """Decrypt a ciphertext using standard RSA"""
    n, d, _, _ = private_key
    return pow(ciphertext, d, n)

def rsa_decrypt_crt(ciphertext, private_key):
    """Decrypt a ciphertext using Chinese Remainder Theorem optimization"""
    n, d, p, q = private_key
    
    # Compute dp = d mod (p-1) and dq = d mod (q-1)
    dp = d % (p - 1)
    dq = d % (q - 1)
    
    # Compute modular exponentiations
    mp = pow(ciphertext, dp, p)
    mq = pow(ciphertext, dq, q)
    
    # Compute qInv = q^(-1) mod p
    qInv = mod_inverse(q, p)
    
    # Apply Chinese Remainder Theorem
    h = (qInv * (mp - mq)) % p
    message = mq + h * q
    
    return message

def compare_decryption_times(bits_list, num_trials=10):
    """Compare the performance of standard RSA decryption vs CRT optimization"""
    print(f"Comparing standard RSA vs CRT-optimized RSA (average of {num_trials} trials)")
    print("-" * 80)
    print(f"{'Key Size':^10} | {'Standard (ms)':^15} | {'CRT (ms)':^15} | {'Speedup':^10}")
    print("-" * 80)
    
    for bits in bits_list:
        total_standard = 0
        total_crt = 0
        
        for _ in range(num_trials):
            # Generate keys
            public_key, private_key = generate_keys(bits)
            
            # Random message
            message = random.randint(2, public_key[0] - 1)
            
            # Encrypt message
            ciphertext = rsa_encrypt(message, public_key)
            
            # Time standard decryption
            start = time.time()
            decrypted_standard = rsa_decrypt_standard(ciphertext, private_key)
            standard_time = (time.time() - start) * 1000  # ms
            
            # Time CRT decryption
            start = time.time()
            decrypted_crt = rsa_decrypt_crt(ciphertext, private_key)
            crt_time = (time.time() - start) * 1000  # ms
            
            # Check correctness
            assert decrypted_standard == decrypted_crt == message, "Decryption error!"
            
            total_standard += standard_time
            total_crt += crt_time
        
        # Calculate averages
        avg_standard = total_standard / num_trials
        avg_crt = total_crt / num_trials
        speedup = avg_standard / avg_crt if avg_crt > 0 else float('inf')
        
        print(f"{bits:^10} | {avg_standard:^15.2f} | {avg_crt:^15.2f} | {speedup:^10.2f}x")

if __name__ == "__main__":
    # Compare for different key sizes
    bits_list = [512, 1024, 2048]  # Add 4096 for more comprehensive comparison if time permits
    compare_decryption_times(bits_list)
