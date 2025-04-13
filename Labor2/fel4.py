# 4. Az alábbi két titkosított szöveg, affin módszerrel volt rejtjelezve, ahol a titkosítást az angol ábécé nagybetűi, a vessző, a pont és a szóköz felett végeztük, összesen M = 29 szimbólumot használva. A nagybetűknek a 0 és 26 közötti számkódokat, a vesszőnek a 26, a pontnak a 27, a szóköznek pedig a 28-as számkódot feleltettük meg. Egyéb írásjeleket nem tartalmazott az eredti fájl. Határozzuk meg mindkét esetben az eredeti szöveget és a rejtjelezéshez használt kulcsot, a következő módszerrel (ismert nyílt szövegű támadás / known plaintext attack):

# Feltételezzük, hogy betűgyakoriság alapján sikerült megállapítani két betű rejtjelezett értékét, azaz tudjuk, hogy x1-nek y1 és az x2-nek az y2 a rejtjele, akkor a következő kongruenciarendszer megoldásával, ahol az ismeretlenek a, b, megállapítható a titkosításhoz használt (a, b) kulcs:
# x1 · a + b = y1 mod M
# x2 · a + b = y2 mod M.
# Az első szöveg esetében tudjuk, hogy A-nak K, és O-nak D a rejtjele.
# A második szöveg esetében tudjuk, hogy I-nek K, és O-nak J a rejtjele.
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

def solve_affine_key(x1, y1, x2, y2, m):
    """
    Solve the congruence system to find affine key (a,b):
    x1 * a + b ≡ y1 (mod m)
    x2 * a + b ≡ y2 (mod m)
    """
    # Subtract the equations to eliminate b
    # (x1 - x2) * a ≡ (y1 - y2) (mod m)
    diff_x = (x1 - x2) % m
    diff_y = (y1 - y2) % m
    
    # Find modular inverse of diff_x
    try:
        diff_x_inv = modinv(diff_x, m)
    except Exception:
        return None, None  # If no inverse exists
    
    # Compute a
    a = (diff_y * diff_x_inv) % m
    
    # Compute b using the first equation
    b = (y1 - a * x1) % m
    
    return a, b

def num_to_char(num, m=29):
    """Convert number to character in our expanded alphabet (A-Z, ',', '.', ' ')"""
    if 0 <= num <= 25:
        return chr(num + ord('A'))
    elif num == 26:
        return ','
    elif num == 27:
        return '.'
    elif num == 28:
        return ' '
    else:
        raise ValueError(f"Invalid number: {num} for alphabet size {m}")

def char_to_num(char, m=29):
    """Convert character to number in our expanded alphabet (A-Z, ',', '.', ' ')"""
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    elif char == ',':
        return 26
    elif char == '.':
        return 27
    elif char == ' ':
        return 28
    else:
        raise ValueError(f"Invalid character: {char} for alphabet size {m}")

def affine_decrypt(ciphertext, a, b, m=29):
    """Decrypt using affine cipher with the given key (a,b) and modulus m"""
    try:
        a_inv = modinv(a, m)
    except Exception:
        return None  # If no modular inverse exists
    
    plaintext = ''
    for char in ciphertext:
        try:
            # Convert character to number
            c = char_to_num(char, m)
            # Apply inverse affine transformation: p = a^-1 * (c - b) mod m
            p = (a_inv * (c - b)) % m
            # Convert back to character
            plaintext += num_to_char(p, m)
        except ValueError:
            # Keep any characters not in our alphabet unchanged
            plaintext += char
    
    return plaintext

def main():
    # Define the alphabet size
    M = 29
    
    # First ciphertext - A->K, O->D
    ciphertext1 = "KZRGQKEGBDFZEKHKBBKHKSKFZFGBMKEGPKBKQKZBMDTHKTDZEDXBMIQPZKZEGTIPDBMGZPVKTIBMZWIXIMPIZWIT,ZEIHRIXGHZAH.,ZVDH.ZEIHEIQPIZKQS.IFAFKPZKYYKSZKMZGXDRDSPYKS,ZKEGFDQZKQS.IFASFZVDBBMKZIH.ISTDZPIBPASFZEKHKBBKHKOKTLLL"
    x1, y1 = char_to_num('A', M), char_to_num('K', M)  # A -> K
    x2, y2 = char_to_num('O', M), char_to_num('D', M)  # O -> D
    
    a1, b1 = solve_affine_key(x1, y1, x2, y2, M)
    if a1 is not None and b1 is not None:
        plaintext1 = affine_decrypt(ciphertext1, a1, b1, M)
        print("First ciphertext:")
        print(f"Key: a={a1}, b={b1}")
        print(f"Decrypted: {plaintext1}")
    else:
        print("Failed to solve for the first key.")
    
    # Second ciphertext - I->K, O->J
    ciphertext2 = "QKMJORJS,GJYUJA,PVNVYTIOAQVO,DVOOVAH,TVS,GJYUJA,OKOLSBOBACNJYIOA,ZIUU,V,DBYBTBORIOAH,VM,JSMNJOJS,DVURIOAH,V,NJXBADBSIOA,BS,BYYBOSMBODIOAH,BURSMJDVY,TKOGVMH,VTKN,BURBGIY,VYAJNIOA,TBUCOBT,NJYIOA,ZIUU,V,NBSNIOAH,V,DVURJOIOAH,V,PKXOBDIOA,BS,V,NKSMNSBUBKOAH,NBPVN,TKOGVMH,VTKN,OBT,BURBGIY,PJMNIOA,YBNXBC,BEKANBNJSM"
    x1, y1 = char_to_num('I', M), char_to_num('K', M)  # I -> K
    x2, y2 = char_to_num('O', M), char_to_num('J', M)  # O -> J
    
    a2, b2 = solve_affine_key(x1, y1, x2, y2, M)
    if a2 is not None and b2 is not None:
        plaintext2 = affine_decrypt(ciphertext2, a2, b2, M)
        print("\nSecond ciphertext:")
        print(f"Key: a={a2}, b={b2}")
        print(f"Decrypted: {plaintext2}")
    else:
        print("Failed to solve for the second key.")

if __name__ == "__main__":
    main() 