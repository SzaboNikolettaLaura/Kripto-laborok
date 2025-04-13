# 1. Írjunk programot, mely Caesar módszerével titkosít és visszafejt egy tetszőleges szövegállományt.
# A szövegállományon végezzünk elő-feldolgozást, oly módon hogy minden betűt alakítsunk nagybetűvé.
# A titkosítást az angol ábécé nagybetűinek megfelelő számkódokon (számkód tábla) végezzük.

def caesar_encryption(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            char = char.upper()
            char = (ord(char) - 65 + shift) % 26 + 65 
            result += chr(char)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encryption(text, -shift)

def file_processing(input_file, output_file, shift, mode):
    try:
        with open(input_file, 'r') as file:
            text = file.read()
        if mode == 'encrypt':
            encrypted_text = caesar_encryption(text, shift)
        elif mode == 'decrypt':
            encrypted_text = caesar_decrypt(text, shift)
        else:
            raise ValueError("Nem letezik a mod amit irtal")
        with open(output_file, 'w') as file:
            file.write(encrypted_text)
    except FileNotFoundError:
        print(f"Error: Nem letezik a file: {input_file}.")
    except IOError:
        print(f"Error: nem lehetett olvasni az input filet: {input_file}.")
    except ValueError as e:
        print(e)

def main():
    input_file = input("input file: ")
    output_file = input("output file: ")
    shift = int(input("Eltolas ertek: "))
    mode = input("Ird be a modot(encrypt/decrypt): ")
    file_processing(input_file, output_file, shift, mode)

if __name__ == "__main__":
    main()



