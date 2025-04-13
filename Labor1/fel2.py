#2. A szöveg Caesar módszerrel volt rejtjelezve, ahol a titkosítást az angol ábécé 26 betűje felett végeztük, a szóközöket és egyéb írásjeleket nem titkosítottuk.
#Határozzuk meg az eredeti szöveget és a rejtjelezéshez használt kulcsot az összes kulcs kipróbálásának módszerével.

def caesar_decrypt(ciphertext):
    for key in range(26):
        decrypted = ""
        for char in ciphertext:
            if char.isalpha():
                shifted = ord(char) - key
                if char.islower():
                    if shifted < ord('a'):
                        shifted += 26
                else:
                    if shifted < ord('A'):
                        shifted += 26
                decrypted += chr(shifted)
            else:
                decrypted += char
        print(f"Key {key}: {decrypted}")

with open('encrypted_text.txt', 'r') as file:
    ciphertext = file.read().strip()
    caesar_decrypt(ciphertext)

