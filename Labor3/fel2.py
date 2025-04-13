import numpy as np

def modular_inverse(a, m):
    """Calculate the modular multiplicative inverse of a modulo m."""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_modular_inverse(matrix, modulus):
    """Calculate the modular multiplicative inverse of a 2x2 matrix."""
    det = int(np.round(np.linalg.det(matrix))) % modulus
    
    # Find modular multiplicative inverse of determinant
    det_inv = modular_inverse(det, modulus)
    
    if det_inv is None:
        raise ValueError("Matrix is not invertible in Z_{}".format(modulus))
    
    # For a 2x2 matrix [[a,b],[c,d]], the adjugate is [[d,-b],[-c,a]]
    adjugate = np.array([
        [matrix[1,1], -matrix[0,1]],
        [-matrix[1,0], matrix[0,0]]
    ])
    
    # Ensure positive values for mod operation
    adjugate = (adjugate % modulus + modulus) % modulus
    
    # Multiply adjugate by det_inv
    inverse = (adjugate * det_inv) % modulus
    
    return inverse

def hill_decrypt(ciphertext, key_matrix, modulus=26):
    """Decrypt a Hill cipher with block size 2."""
    # Remove any whitespace
    ciphertext = ciphertext.strip()
    
    # Convert key matrix to numpy array
    key_matrix = np.array(key_matrix).reshape(2, 2)
    
    # Calculate inverse key matrix
    inverse_key = matrix_modular_inverse(key_matrix, modulus)
    
    # Convert ciphertext to numerical values (A=0, B=1, ..., Z=25)
    cipher_nums = [ord(c) - ord('A') for c in ciphertext]
    
    # Decrypt in blocks of 2
    plain_nums = []
    for i in range(0, len(cipher_nums), 2):
        if i+1 < len(cipher_nums):
            # Get a block of 2 characters
            block = np.array([cipher_nums[i], cipher_nums[i+1]])
            
            # Multiply by inverse key matrix
            decrypted_block = np.dot(inverse_key, block) % modulus
            
            # Add to plaintext
            plain_nums.extend(decrypted_block)
    
    # Convert numerical values back to letters
    plaintext = ''.join([chr(num + ord('A')) for num in plain_nums])
    
    return plaintext

# Given information
ciphertext = "AOGWEPOFKHSVRWYUKDAZKVYYNGYPQFKAWROZIEATIYROLMYYOSNRLIACOFJAGIUT"
key = [6, 13, 7, 8]  # Key matrix: [[6, 13], [7, 8]]

# Decrypt the ciphertext
plaintext = hill_decrypt(ciphertext, key)
print(f"Ciphertext: {ciphertext}")
print(f"Plaintext: {plaintext}")
