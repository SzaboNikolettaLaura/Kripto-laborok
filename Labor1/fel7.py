#7. Az alábbi titkosított szöveg Keyword Caesar módszerrel volt rejtjelezve, ahol a titkosítást az angol ábécé 26 betűje felett végeztük, a szóközöket és egyéb írásjeleket nem titkosítottuk. Határozzuk meg az eredeti szöveget, betűgyakoriság vizsgálattal (angol betűgyakoriság tábla), illetve határozzuk meg a rejtjelezéshez használt kulcsot.
def count_letter_frequency(text):
    # Only count alphabetic characters
    frequency = {}
    total = 0
    for char in text:
        if char.isalpha():
            char = char.upper()
            frequency[char] = frequency.get(char, 0) + 1
            total += 1
    
    # Convert to percentages
    for char in frequency:
        frequency[char] = (frequency[char] / total) * 100
    
    # Sort by frequency
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq, total

def count_ngrams(text, n):
    ngrams = {}
    text = ''.join(c for c in text.upper() if c.isalpha() or c == ' ')
    
    for i in range(len(text) - n + 1):
        if ' ' not in text[i:i+n]:  # Skip ngrams with spaces
            ngram = text[i:i+n]
            if len(ngram) == n:
                ngrams[ngram] = ngrams.get(ngram, 0) + 1
    
    # Sort by frequency
    sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
    return sorted_ngrams

def find_common_words(text):
    word_freq = {}
    text = ''.join(c if c.isalpha() or c.isspace() else ' ' for c in text.upper())
    words = text.split()
    
    for word in words:
        if len(word) >= 2:  # Only count words with length >= 2
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_words

def create_keyword_table(keyword):
    keyword = keyword.upper()
    seen = set()
    table = []
    for c in keyword:
        if c not in seen and c.isalpha():
            seen.add(c)
            table.append(c)
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if c not in seen:
            table.append(c)
    return table

def count_ngram_matches(text, ngram):
    """Count how many times an ngram appears in the text"""
    return text.upper().count(ngram.upper())

def decrypt(text, keyword, shift):
    table = create_keyword_table(keyword)
    result = []
    for c in text:
        if c.isalpha():
            idx = table.index(c)
            new_idx = (idx - shift) % 26
            result.append(table[new_idx])
        else:
            result.append(c)
    return ''.join(result)


def english_letter_frequencies():
    """Return standard English letter frequencies."""
    return {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 
        'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 
        'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
    }

def get_english_common_ngrams():
    """Return the most common 2-letter and 3-letter combinations in English."""
    two_letter = {
        "TH": 3.88, "HE": 3.68, "IN": 2.28, "ER": 2.17, "AN": 2.14,
        "RE": 1.74, "ND": 1.57, "ON": 1.41, "EN": 1.38, "AT": 1.33,
        "OU": 1.28, "ED": 1.27, "HA": 1.27, "TO": 1.16, "OR": 1.15,
        "IT": 1.13, "IS": 1.10, "HI": 1.09, "ES": 1.09, "NG": 1.05
    }
    
    three_letter = {
        "THE": 3.50, "AND": 1.593, "ING": 1.147, "HER": 0.822, "HAT": 0.650,
        "HIS": 0.596, "THA": 0.593, "ERE": 0.560, "FOR": 0.555, "ENT": 0.530,
        "ION": 0.506, "TER": 0.461, "WAS": 0.460, "YOU": 0.437, "ITH": 0.431,
        "VER": 0.430, "ALL": 0.422, "WIT": 0.397, "THI": 0.394, "TIO": 0.378
    }
    
    return two_letter, three_letter

ciphertext = """GUR TERRXF BS GUR PYNFFVPNY REN ZNQR FRIRENY ABGNOYR PBAGEVOHGVBAF GB FPVRAPR NAQ URYCRQ YNL GUR SBHAQNGVBAF BS FRIRENY JRFGREA FPVRAGVSVP GENQVGVBAF, YVXR CUVYBFBCUL, UVFGBEVBTENCUL NAQ ZNGURZNGVPF. GUR FPUBYNEYL GENQVGVBA BS GUR TERRX NPNQRZVRF JNF ZNVAGNVARQ QHEVAT EBZNA GVZRF JVGU FRIRENY NPNQRZVP VAFGVGHGVBAF VA PBAFGNAGVABCYR, NAGVBPU, NYRKNAQEVN NAQ BGURE PRAGERF BS TERRX YRNEAVAT JUVYR RNFGREA EBZNA FPVRAPR JNF RFFRAGVNYYL N PBAGVAHNGVBA BS PYNFFVPNY FPVRAPR. TERRXF UNIR N YBAT GENQVGVBA BS INYHVAT NAQ VAIRFGVAT VA CNVQRVN (RQHPNGVBA). CNVQRVN JNF BAR BS GUR UVTURFG FBPVRGNY INYHRF VA GUR TERRX NAQ URYYRAVFGVP JBEYQ JUVYR GUR SVEFG RHEBCRNA VAFGVGHGVBA QRFPEVORQ NF N HAVIREFVGL JNF SBHAQRQ VA PBAFGNAGVABCYR NAQ BCRENGRQ VA INEVBHF VAPNEANGVBAF."""
def main():
    # Direct input of ciphertext

    print("Analyzing ciphertext using ngrams...")
    
    # Define the n-grams to test
    two_letter_ngrams = [
        "TH", "HE", "IN", "ER", "AN", "RE", "ND", "ON", "EN", "AT", 
        "OU", "ED", "HA", "TO", "OR", "IT", "IS", "HI", "ES", "NG"
    ]
    
    three_letter_ngrams = [
        "THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "FOR", "ENT",
        "ION", "TER", "WAS", "YOU", "ITH", "VER", "ALL", "WIT", "THI", "TIO"
    ]
    
    all_ngrams = two_letter_ngrams + three_letter_ngrams
    
    # Test each ngram
    results = []
    
    print("Testing all ngrams one by one with all possible shifts...")
    for ngram in all_ngrams:
        best_shift = 0
        best_count = -1
        best_decrypted = ""
        
        # Try all possible shifts for this ngram
        for shift in range(26):
            decrypted = decrypt(ciphertext, ngram, shift)
            
            # Count how many times this ngram appears in the decrypted text
            count = count_ngram_matches(decrypted, ngram)
            
            if count > best_count:
                best_count = count
                best_shift = shift
                best_decrypted = decrypted
        
        # Store results
        results.append({
            'ngram': ngram,
            'shift': best_shift,
            'count': best_count,
            'decrypted': best_decrypted
        })
        
        print(f"Ngram: {ngram}, Best Shift: {best_shift}, Matches: {best_count}")
    
    # Sort by count (higher is better)
    results.sort(key=lambda x: x['count'], reverse=True)
    
    print("\nTop 5 results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. Keyword: {result['ngram']}, Shift: {result['shift']}, Matches: {result['count']}")
        print(f"   Sample: {result['decrypted'][:100]}")
    
    best_result = results[0]
    print(f"\nBest keyword appears to be: {best_result['ngram']} with shift {best_result['shift']}")
    print("\nDecrypted text:")
    print(best_result['decrypted'])
    
    # Print the keyword and how it maps
    keyword = best_result['ngram']
    shift = best_result['shift']
    key_alphabet = create_keyword_table(keyword)
    
    print("\nSolution:")
    print(f"Keyword: {keyword}")
    print(f"Shift: {shift}")
    print(f"Standard alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print(f"Cipher alphabet:   {key_alphabet}")

if __name__ == "__main__":
    main()