#1. Írjunk programot, amely háromféle módszerrel is meghatározza a multiplikatív inverzét mod b szerint. A három módszer a következő legyen:
#az összes érték kipróbálásának módszere
#a bináris kiterjesztett Eukleidészi algoritmus
#a kis-Fermat tételén (ha b prímszám), Euler tételén (tetszőleges b-re) alapuló algoritmus
def bruteforce_inverse(a, b):
    """Find multiplicative inverse of a mod b using brute force method"""
    for x in range(1, b):
        if (a * x) % b == 1:
            return x
    return None

def extended_gcd(a, b):
    """Extended Euclidean algorithm for gcd(a,b) and Bézout coefficients"""
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def fermat_euler_inverse(a, b):
    """Find multiplicative inverse using Fermat's Little Theorem or Euler's Theorem"""
    # Check if gcd(a,b) = 1
    gcd, _, _ = extended_gcd(a, b)
    if gcd != 1:
        return None
    
    # Calculate Euler's totient (phi) function
    def phi(n):
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result
    
    # Calculate using Euler's theorem: a^(φ(b)-1) ≡ a^(-1) (mod b)
    return pow(a, phi(b) - 1, b)

def main():
    # Get input from user
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    
    # Check if gcd(a,b) = 1
    gcd, x, y = extended_gcd(a, b)
    if gcd != 1:
        print(f"The multiplicative inverse doesn't exist because gcd({a},{b}) = {gcd} ≠ 1")
        return
    
    # Method 1: Brute force
    inv1 = bruteforce_inverse(a, b)
    print(f"Method 1 (Brute force): The multiplicative inverse of {a} mod {b} is {inv1}")
    
    # Method 2: Extended Euclidean algorithm
    # Make sure the result is positive
    inv2 = x % b
    print(f"Method 2 (Extended Euclidean): The multiplicative inverse of {a} mod {b} is {inv2}")
    
    # Method 3: Fermat's Little Theorem or Euler's Theorem
    inv3 = fermat_euler_inverse(a, b)
    print(f"Method 3 (Fermat/Euler): The multiplicative inverse of {a} mod {b} is {inv3}")

if __name__ == "__main__":
    main() 