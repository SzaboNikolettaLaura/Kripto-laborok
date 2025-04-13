#6. Írjunk programot, mely a Keyword Caesar módszerével titkosít és visszafejt egy tetszőleges szövegállományt. A szövegállományon végezzünk elő-feldolgozást, oly módon hogy minden betűt alakítsunk nagybetűvé. A titkosítást az angol ábécé nagybetűinek megfelelő számkódokon (számkód tábla) végezzük.
import sys

def preprocess(text):
    return text.upper()

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

def encrypt(text, keyword, shift):
    table = create_keyword_table(keyword)
    result = []
    for c in text:
        if c.isalpha():
            idx = table.index(c)
            new_idx = (idx + shift) % 26
            result.append(table[new_idx])
        else:
            result.append(c)
    return ''.join(result)

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

def main():
    if len(sys.argv) != 6:
        print("Usage: python fel6.py <input_file> <output_file> <keyword> <shift> <mode>")
        print("mode: 'encrypt' or 'decrypt'")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    keyword = sys.argv[3]
    shift = int(sys.argv[4])
    mode = sys.argv[5]
    with open(input_file, 'r') as f:
        text = f.read()
    processed = preprocess(text)
    if mode == 'encrypt':
        result = encrypt(processed, keyword, shift)
    elif mode == 'decrypt':
        result = decrypt(processed, keyword, shift)
    else:
        print("Invalid mode. Use 'encrypt' or 'decrypt'")
        sys.exit(1)
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"{mode.capitalize()}ed text written to {output_file}")

if __name__ == "__main__":
    main() 