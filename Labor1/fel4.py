import sys

def is_valid_text(text):
    for c in text:
        if not (32 <= ord(c) <= 126 or ord(c) in [10, 13]):
            return False
    return True

def caesar_decrypt(data, key):
    return bytes((b - key) % 256 for b in data)

def main():
    if len(sys.argv) != 2:
        print("Usage: python fel4.py <input_file>")
        return

    input_file = sys.argv[1]
    try:
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
    except IOError:
        print(f"Error: Could not open file {input_file}")
        return

    for key in range(256):
        decrypted_data = caesar_decrypt(encrypted_data, key)
        decrypted_text = decrypted_data.decode('latin1')
        if is_valid_text(decrypted_text):
            print(f"Key: {key}")
            print("Decrypted text:")
            print(decrypted_text)
            print("-" * 50)

if __name__ == "__main__":
    main() 