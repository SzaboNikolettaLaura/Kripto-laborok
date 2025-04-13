#2. Írjunk programot, mely affin módszerrel titkosít és visszafejt egy tetszőleges szövegállományt. A szövegállományon végezzünk elő-feldolgozást, oly módon hogy minden betűt alakítsunk nagybetűvé, és csak az angol ábécé betűit tartsuk meg, a többi karaktert vágjuk ki, majd az így kapott szöveg angol ábécé nagybetűinek feleltessük meg a megfelelő számkódokat (számkód tábla). A titkosítást a számkódokon végezzük.
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

def preprocess_text(text):
    # Convert to uppercase and remove non-alphabetic characters
    result = ''
    for char in text:
        if char.isalpha():
            result += char.upper()
    return result

def char_to_num(char):
    # Convert character to number (A=0, B=1, ..., Z=25)
    return ord(char) - ord('A')

def num_to_char(num):
    # Convert number to character (0=A, 1=B, ..., 25=Z)
    return chr(num % 26 + ord('A'))

def affine_encrypt(plaintext, a, b):
    # Check if 'a' is valid (gcd(a, 26) = 1)
    if extended_gcd(a, 26)[0] != 1:
        raise ValueError("Invalid 'a' parameter. Must be coprime with 26.")
    
    # Preprocess the input text
    plaintext = preprocess_text(plaintext)
    
    ciphertext = ''
    for char in plaintext:
        # Convert character to number
        m = char_to_num(char)
        # Apply affine transformation: c = (am + b) mod 26
        c = (a * m + b) % 26
        # Convert back to character
        ciphertext += num_to_char(c)
    
    return ciphertext

def affine_decrypt(ciphertext, a, b):
    # Check if 'a' is valid (gcd(a, 26) = 1)
    if extended_gcd(a, 26)[0] != 1:
        raise ValueError("Invalid 'a' parameter. Must be coprime with 26.")
    
    # Calculate the modular multiplicative inverse of 'a'
    a_inv = modinv(a, 26)
    
    plaintext = ''
    for char in ciphertext:
        # Convert character to number
        c = char_to_num(char)
        # Apply inverse affine transformation: m = a^-1 * (c - b) mod 26
        m = (a_inv * (c - b)) % 26
        # Convert back to character
        plaintext += num_to_char(m)
    
    return plaintext

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def write_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File saved successfully to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    print("Affine Cipher Program")
    mode = input("Mode (encrypt/decrypt): ").lower()
    
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode! Please choose 'encrypt' or 'decrypt'.")
        return
    
    input_file = input("Input file: ")
    output_file = input("Output file: ")
    
    try:
        a = int(input("Enter 'a' parameter (must be coprime with 26): "))
        b = int(input("Enter 'b' parameter: "))
        
        if extended_gcd(a, 26)[0] != 1:
            print("Error: 'a' parameter must be coprime with 26!")
            return
        
        text = read_file(input_file)
        
        if mode == 'encrypt':
            result = affine_encrypt(text, a, b)
        else:  # decrypt
            # Preprocess the ciphertext (in case it contains non-alphabetic characters)
            text = preprocess_text(text)
            result = affine_decrypt(text, a, b)
        
        write_file(output_file, result)
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 