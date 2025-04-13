import re

def char_to_num(c):
    return 26 if c == ' ' else ord(c) - ord('a')

def num_to_char(n):
    return ' ' if n % 27 == 26 else chr(n % 27 + ord('a'))

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_inv_2x2(m, mod=27):
    det = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % mod
    det_inv = mod_inverse(det, mod)
    return [
        [(m[1][1] * det_inv) % mod, (-m[0][1] * det_inv) % mod],
        [(-m[1][0] * det_inv) % mod, (m[0][0] * det_inv) % mod]
    ]

def matrix_mul(A, B, mod=27):
    return [
        [sum((A[i][k] * B[k][j]) % mod for k in range(len(B))) % mod
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]

def decrypt_hill(ciphertext, key_matrix, mod=27):
    ciphertext = re.sub(r'[^a-z ]', '', ciphertext.lower())
    if len(ciphertext) % 2:
        ciphertext += 'x'

    num_text = [char_to_num(c) for c in ciphertext]
    plaintext = ""

    for i in range(0, len(num_text), 2):
        block = [[num_text[i]], [num_text[i+1]]]
        dec_block = matrix_mul(key_matrix, block, mod)
        plaintext += num_to_char(dec_block[0][0]) + num_to_char(dec_block[1][0])

    return plaintext

if __name__ == "__main__":
    plain_pairs, cipher_pairs = ["pu", "or"], ["oa", "we"]

    P = [
        [char_to_num(plain_pairs[0][0]), char_to_num(plain_pairs[1][0])],
        [char_to_num(plain_pairs[0][1]), char_to_num(plain_pairs[1][1])]
    ]

    C = [
        [char_to_num(cipher_pairs[0][0]), char_to_num(cipher_pairs[1][0])],
        [char_to_num(cipher_pairs[0][1]), char_to_num(cipher_pairs[1][1])]
    ]

    K = matrix_mul(C, matrix_inv_2x2(P))
    K_inv = matrix_inv_2x2(K)

    print("Decryption matrix (K^-1):", K_inv)
    try:
        with open("outHill.txt", "r") as file:
            cyphertext = file.read().strip()
            plaintext = decrypt_hill(cyphertext, K_inv)
            print("Decrypted text:", plaintext)
    except FileNotFoundError:
        print("File not found. Please ensure 'outHill.txt' exists in the current directory.")
