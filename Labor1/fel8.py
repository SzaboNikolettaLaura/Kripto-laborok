def find_mapping(ciphertext, plaintext):
    """Find possible mapping from ciphertext to plaintext characters"""
    mapping = {}
    reverse_mapping = {}
    
    # Split into words to analyze structure
    cipher_words = ciphertext.split()
    plain_words = plaintext.split()
    
    # Check if word count matches
    if len(cipher_words) != len(plain_words):
        return None
    
    # Check if word lengths match
    for i, (cipher_word, plain_word) in enumerate(zip(cipher_words, plain_words)):
        if len(cipher_word) != len(plain_word):
            return None
    
    # Try to build the substitution map
    for c, p in zip(ciphertext, plaintext):
        if c == ' ' and p == ' ':
            continue
            
        if c in mapping:
            # This cipher character was already mapped
            if mapping[c] != p:
                return None  # Inconsistent mapping
        elif p in reverse_mapping:
            # This plain character was already mapped to
            if reverse_mapping[p] != c:
                return None  # Inconsistent mapping
        else:
            # New mapping
            mapping[c] = p
            reverse_mapping[p] = c
    
    return mapping

def decrypt(ciphertext, mapping):
    """Decrypt text using the provided mapping"""
    result = ""
    for c in ciphertext:
        if c == ' ':
            result += ' '
        elif c in mapping:
            result += mapping[c]
        else:
            # Character not in mapping, keep as is
            result += c
    return result

def complete_mapping(partial_mapping):
    """Complete a partial mapping to cover all lowercase letters"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    reverse_mapping = {v: k for k, v in partial_mapping.items()}
    
    # Find unused cipher and plain characters
    unused_cipher = [c for c in alphabet if c not in partial_mapping]
    unused_plain = [c for c in alphabet if c not in reverse_mapping]
    
    # Create a complete mapping by connecting unused characters
    if len(unused_cipher) != len(unused_plain):
        return None
        
    for c, p in zip(unused_cipher, unused_plain):
        partial_mapping[c] = p
        
    return partial_mapping

def solve_case(lines):
    known_plaintext = "the quick brown fox jumps over the lazy dog"
    
    # Try each line as the known plaintext
    for known_line in lines:
        mapping = find_mapping(known_line, known_plaintext)
        if mapping is None:
            continue
            
        # Complete the mapping to cover all lowercase letters
        complete_mapping(mapping)
        
        # Try to decrypt all lines with this mapping
        decrypted = [decrypt(line, mapping) for line in lines]
        
        # Check if the decryption contains only valid characters
        valid = True
        for line in decrypted:
            for c in line:
                if c != ' ' and not ('a' <= c <= 'z'):
                    valid = False
                    break
            if not valid:
                break
                
        if valid:
            return decrypted
    
    return ["No solution"]

def main():
    try:
        with open("lab8_input.txt", "r") as file:
            lines = file.read().strip().split('\n')
    except:
        # If file can't be opened, read from standard input
        import sys
        lines = sys.stdin.read().strip().split('\n')
    
    num_cases = int(lines[0])
    
    case_start = 2  # Skip the first line (num_cases) and the empty line
    results = []
    
    for _ in range(num_cases):
        case_lines = []
        while case_start < len(lines) and lines[case_start] != '':
            case_lines.append(lines[case_start])
            case_start += 1
        
        # Process this case
        case_result = solve_case(case_lines)
        results.append(case_result)
        
        # Skip the empty line between cases
        case_start += 1
    
    # Output results
    for i, case_result in enumerate(results):
        if i > 0:
            print()  # Empty line between cases
        for line in case_result:
            print(line)

if __name__ == "__main__":
    main()
