# 1. Írjunk programot, mely Caesar módszerével titkosít és visszafejt egy tetszőleges szövegállományt.
# A szövegállományon végezzünk elő-feldolgozást, oly módon hogy minden betűt alakítsunk nagybetűvé.
# A titkosítást az angol ábécé nagybetűinek megfelelő számkódokon (számkód tábla) végezzük.


def caesar_encryption(text, shift):
    result = ""
    for char in text: #vegig megyunk a szovegen, beturol beture
        if char.isalpha(): #megnezzuk, ha betu-e a karakter
            char = char.upper() #ha betu, akkor nagybeture alakitjuk
            char = (ord(char) - 65 + shift) % 26 + 65 
#                      ^         ^     ^       ^    ^
#                      |         |     |       |    |
#                      |         |     |       |    hozzaadunk 65-t hogy megkapjuk a karakter ASCII kodjat
#                      |         |     |       |
#                      |         |     |       Mivel csak angol ABC betukkel dolgozunk, ezert meg kell oljduk, hogy maradjunk a 0 es 25 kozott. 
#                      |         |     |       a %26-al valo osztas ezt biztositja. Ettol lesz korkoros, pl ha a szam amit kapunk 27 lesz,
#                      |         |     |       akkor a 27 % 26 = 1 lesz, ami a B betunak felel meg.
#                      |         |     |
#                      |         |     A szam amivel el volt tolva az algoritmus a shift.
#                      |         |
#                      |         Kivonjuk a 65-ot hogy visszakapjuk a karakter ASCII kodjat.
#                      |         Ekkor a 0 az A betunak felel meg, 1 a B betunak, stb. Igy konnyen tudjuk shiftelni a betuket, az mondjuk meg mennyivel menjunk tovabb
#                      |
#                      A betut szamma alakitjuk, dehat az "A" 65-e alakitja, a "B" 66-a, stb, hogy tudjuk shiftelni a betuket
        else:           #en itt lekezeltem, ha nem betu, akkor hagyja beken, es adja hozza a stringhez amit visszateritek
            result += char
    return result       #visszateritem az atalakitott stringet

def caesar_decrypt(text, shift):
    #igazabol a visszafejtes ugyanugy mukodik, mint a titkositas, csak a shiftet negativra valtozzuk
    #basically visszafele tolunk
    return caesar_encrypt(text, -shift)

def file_processing(input_file, output_file, shift, mode):
#fuggveny parameterei:
#input_file: a szoveg amit titkositani akarunk
#output_file: a szoveg amit kapunk titkositas utan hova irja ki
#shift: amivel tuljuk a betuket
#mode: enkriptaljuk vagy dekriptaljuk
    try:
        with open(input_file, 'r') as file:
            text = file.read()
        if mode == 'encrypt':
            encrypted_text = caesar_encrypt(text, shift)
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
    #beolvassuk a parancssorbol a fuggveny parametereit
    input_file = input("input file: ")
    output_file = input("output file: ")
    shift = int(input("Eltolas ertek: "))
    mode = input("Ird be a modot(encrypt/decrypt): ")
    file_processing(input_file, output_file, shift, mode)

if __name__ == "__main__":
    main()



