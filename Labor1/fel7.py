import random


def frequencyAnalyzer(str):
    dict = {}
    # going through each character of the string
    for c in str:
        # if the character is an alphabetic, we will count the appearances.
        if((c >= 'a' and c<='z') or (c >= 'A' and c<= 'Z') ):
            c = c.lower()
            
            if(dict.get(c) != None):
                dict[c] +=1
            else:
                dict[c] = 1
    
    # Convert counts to sorted list of tuples
    sorted_items = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def txtToString(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # English letter frequency table in descending order of frequency
    english_frequency_ordered = [
        'e', 't', 'a', 'o', 'n', 'i', 's', 'r', 'h', 'l',
        'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b',
        'v', 'k', 'x', 'j', 'q', 'z'
    ]
    
    encryptedMessage = "NEW SLWWCM HI NEW YDVMMAYVD WLV FVZW MWPWLVD GHNVXDWYHGNLAXONAHGM NH MYAWGYW VGZ EWDJWZ DVT NEW IHOGZVNAHGM HI MWPWLVD QWMNWLG MYAWGNAIAY NLVZANAHGM, DACW JEADHMHJET, EAMNHLAHSLVJET VGZ FVNEWFVNAYM. NEW MYEHDVLDT NLVZANAHG HI NEW SLWWC VYVZWFAWM QVM FVAGNVAGWZ ZOLAGS LHFVG NAFWM QANE MWPWLVD VYVZWFAY AGMNANONAHGM AG YHGMNVGNAGHJDW, VGNAHYE, VDWRVGZLAV VGZ HNEWL YWGNLWM HI SLWWC DWVLGAGS QEADW WVMNWLG LHFVG MYAWGYW QVM WMMWGNAVDDT V YHGNAGOVNAHG HI YDVMMAYVD MYAWGYW. SLWWCM EVPW V DHGS NLVZANAHG HI PVDOAGS VGZ AGPWMNAGS AG JVAZWAV (WZOYVNAHG). JVAZWAV QVM HGW HI NEW EASEWMN MHYAWNVD PVDOWM AG NEW SLWWC VGZ EWDDWGAMNAY QHLDZ QEADW NEW IALMN WOLHJWVG AGMNANONAHG ZWMYLAXWZ VM V OGAPWLMANT QVM IHOGZWZ AG 5NE YWGNOLT YHGMNVGNAGHJDW VGZ HJWLVNWZ AG PVLAHOM AGYVLGVNAHGM OGNAD NEW YANT'M IVDD NH NEW HNNHFVGM AG 1453."

    # obtaining the letters frequency from encrypted text
    encryptedMessageWordsFrequency = frequencyAnalyzer(encryptedMessage)
    
    # Print frequency analysis of encrypted text
    print("Frequency analysis of the encrypted text:")
    for char, count in encryptedMessageWordsFrequency[:10]:
        print(f"'{char}': {count}")
    
    # Get most frequent letter in encrypted text
    most_frequent_encrypted = encryptedMessageWordsFrequency[0][0] if encryptedMessageWordsFrequency else 'e'
    print("\nMost frequent letter in encrypted text:", most_frequent_encrypted)
    
    print("\nTrying all letters from the english frequency table as possible keys:")
    print("-" * 80)
    
    # Try all letters from the frequency table
    for reference_letter in english_frequency_ordered:
        # Calculate the shift
        shift_distance = (ord(most_frequent_encrypted) - ord(reference_letter)) % 26
        
        # decrypt using the calculated key
        decryptedMessage = decrypt(encryptedMessage, shift_distance)
        
        # Display a preview of the decrypted message
        preview = decryptedMessage[:100] + "..." if len(decryptedMessage) > 100 else decryptedMessage
        
        print(f"If '{most_frequent_encrypted}' maps to '{reference_letter}' (shift {shift_distance}):")
        print(preview)
        print("-" * 80)

if __name__ == "__main__":
    main()
