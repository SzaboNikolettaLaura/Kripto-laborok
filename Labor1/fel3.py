#3. A klasszikus Caesar módszere az angol (latin) ábécé felett végzi a titkosítást. Írjunk programot, amely a Caesar titkosítást/visszafejtést bináris állományokon, bájtok felett végzi.

def caesar_encrypt(input_file, output_file, shift):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(1024)
            if not chunk:
                break
            encrypted_chunk = bytes((b + shift) % 256 for b in chunk)
            f_out.write(encrypted_chunk)

def caesar_decrypt(input_file, output_file, shift):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(1024)
            if not chunk:
                break
            decrypted_chunk = bytes((b - shift) % 256 for b in chunk)
            f_out.write(decrypted_chunk)

def main():
    import sys
    if len(sys.argv) != 5:
        print("Usage: python fel3.py <encrypt/decrypt> <input_file> <output_file> <shift>")
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    shift = int(sys.argv[4])

    if operation == 'encrypt':
        caesar_encrypt(input_file, output_file, shift)
    elif operation == 'decrypt':
        caesar_decrypt(input_file, output_file, shift)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'")
        sys.exit(1)

if __name__ == "__main__":
    main()