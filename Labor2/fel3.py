#3. Az alábbi titkosított szöveg, affin módszerrel volt rejtjelezve, ahol a titkosítást az angol ábécé 26 betűje felett végeztük, és az angol ábécé betűin kívül más írásjelet nem titkosítottunk. Határozzuk meg az eredeti szöveget és a kulcspárt, az összes lehetséges kulcs kipróbálásának módszerével, tudva azt, hogy az eredeti szöveg egy magyar szöveg, amely tartalmazza az AZ szót.

#EX GKLGTGWRGW BE HGDPGAODRG KIRZEX EKIH WIVERREW, RGK VEDRE E PEVOWTE. BGTEWDGIHYAX
import re

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
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def char_to_num(char):
    # Convert character to number (A=0, B=1, ..., Z=25)
    return ord(char) - ord('A')

def num_to_char(num):
    # Convert number to character (0=A, 1=B, ..., 25=Z)
    return chr(num % 26 + ord('A'))

def affine_decrypt(ciphertext, a, b):
    # Calculate the modular multiplicative inverse of 'a'
    try:
        a_inv = modinv(a, 26)
    except:
        return None  # If no modular inverse exists
    
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            # Convert character to number
            c = char_to_num(char)
            # Apply inverse affine transformation: m = a^-1 * (c - b) mod 26
            m = (a_inv * (c - b)) % 26
            # Convert back to character
            plaintext += num_to_char(m)
        else:
            plaintext += char
    
    return plaintext

def brute_force_affine(ciphertext, target_word="AZ"):
    valid_a_values = []
    for a in range(1, 26):
        if extended_gcd(a, 26)[0] == 1:  # Check if a is coprime with 26
            valid_a_values.append(a)
    
    results = []
    for a in valid_a_values:
        for b in range(26):
            decrypted = affine_decrypt(ciphertext, a, b)
            if decrypted and re.match(f"\\b{target_word}\\b", decrypted):
                results.append((a, b, decrypted))
    
    return results

def main():
    ciphertext = "EX GKLGTGWRGW BE HGDPGAODRG KIRZEX EKIH WIVERREW, RGK VEDRE E PEVOWTE. BGTEWDGIHYAX"
    
    print("Trying all possible affine cipher keys to find Hungarian text containing 'AZ'...")
    possible_decryptions = brute_force_affine(ciphertext)
    
    if possible_decryptions:
        print(f"Found {len(possible_decryptions)} possible decryptions:")
        for i, (a, b, decrypted) in enumerate(possible_decryptions, 1):
            print(f"\n{i}. Key: a={a}, b={b}")
            print(f"Decrypted text: {decrypted}")
    else:
        print("No valid decryption found containing 'AZ'.")

if __name__ == "__main__":
    main() 