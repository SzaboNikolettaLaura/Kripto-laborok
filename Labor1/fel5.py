#5. A szövegállományban található szöveg Caesar módszerrel volt rejtjelezve, ahol a titkosítást az angol ábécé kis és nagybetűje plusz a kérdőjel és szóköz felett végeztük, összesen 54 szimbólumot használva. A kisbetűknek a 0 és 25 közötti számkódokat, a nagybetűknek a 26 és 51 közöttieket, a kérdőjelnek az 52, a szóköznek pedig az 53 számkódot feleltettük meg. Egyéb írásjeleket nem tartalmazott az eredti fájl. Határozzuk meg az eredeti szöveget és a rejtjelezéshez használt kulcsot az összes kulcs kipróbálásának módszerével.
import sys

def char_to_code(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    elif 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 26
    elif c == '?':
        return 52
    elif c == ' ':
        return 53
    return None

def code_to_char(code):
    if 0 <= code <= 25:
        return chr(code + ord('a'))
    elif 26 <= code <= 51:
        return chr(code - 26 + ord('A'))
    elif code == 52:
        return '?'
    elif code == 53:
        return ' '
    return None

def is_valid_text(text):
    for c in text:
        if char_to_code(c) is None:
            return False
    return True

def caesar_decrypt(text, key):
    result = []
    for c in text:
        code = char_to_code(c)
        if code is not None:
            decrypted_code = (code - key) % 54
            result.append(code_to_char(decrypted_code))
    return ''.join(result)

def main():
    if len(sys.argv) != 2:
        print("Usage: python fel5.py <input_file>")
        return

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()
    except IOError:
        print(f"Error: Could not open file {input_file}")
        return

    for key in range(54):
        decrypted_text = caesar_decrypt(encrypted_text, key)
        if is_valid_text(decrypted_text):
            print(f"Key: {key}")
            print("Decrypted text:")
            print(decrypted_text)
            print("-" * 50)

if __name__ == "__main__":
    main() 