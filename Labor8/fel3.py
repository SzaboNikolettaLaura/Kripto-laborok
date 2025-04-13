#3. Generáljunk véletlenszerűen 2048 bites Diffie-Hellman publikus paramétert, mentsük ki a generált értékeket egy állományba, majd ezeket felhasználva a Schnorr aláírási sémát alkalmazva határozzuk meg egy tetszőleges bájtszekvencia digitális aláírását, illetve ellenőrizzük le a létrehozott aláírást.
import os
import random
import hashlib
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Generate 2048-bit Diffie-Hellman parameters
def generate_dh_params():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

# Save DH parameters to file
def save_dh_params(parameters, filename):
    p = parameters.parameter_numbers().p
    g = parameters.parameter_numbers().g
    
    with open(filename, 'w') as f:
        f.write(f"p = {p}\n")
        f.write(f"g = {g}\n")
    
    return p, g

# Generate private and public keys for Schnorr signature
def generate_schnorr_keys(p, g):
    # Private key: random number between 1 and p-1
    x = random.randint(1, p-2)
    # Public key: g^x mod p
    y = pow(g, x, p)
    
    return x, y

# Schnorr signature generation
def schnorr_sign(message, p, g, private_key):
    # Convert message to bytes if it's not already
    if isinstance(message, str):
        message = message.encode()
    
    # Choose a random k (ephemeral key) between 1 and p-1
    k = random.randint(1, p-2)
    
    # Calculate r = g^k mod p
    r = pow(g, k, p)
    
    # Calculate e = H(message || r)
    hash_input = message + str(r).encode()
    e = int(hashlib.sha256(hash_input).hexdigest(), 16) % p
    
    # Calculate s = (k - private_key * e) mod (p-1)
    s = (k - private_key * e) % (p-1)
    
    return (e, s)

# Schnorr signature verification
def schnorr_verify(message, signature, p, g, public_key):
    e, s = signature
    
    # Convert message to bytes if it's not already
    if isinstance(message, str):
        message = message.encode()
    
    # Calculate g^s * y^e mod p
    rv = (pow(g, s, p) * pow(public_key, e, p)) % p
    
    # Calculate e' = H(message || rv)
    hash_input = message + str(rv).encode()
    ev = int(hashlib.sha256(hash_input).hexdigest(), 16) % p
    
    # Signature is valid if e equals e'
    return e == ev

def main():
    # Generate DH parameters
    print("Generating 2048-bit Diffie-Hellman parameters...")
    parameters = generate_dh_params()
    
    # Save parameters to file
    params_file = "dh_params.txt"
    p, g = save_dh_params(parameters, params_file)
    print(f"DH parameters saved to {params_file}")
    
    # Generate Schnorr keys
    private_key, public_key = generate_schnorr_keys(p, g)
    
    # Save keys to file
    keys_file = "schnorr_keys.txt"
    with open(keys_file, 'w') as f:
        f.write(f"private_key = {private_key}\n")
        f.write(f"public_key = {public_key}\n")
    print(f"Schnorr keys saved to {keys_file}")
    
    # Create a sample message
    message = b"This is a test message for Schnorr signature"
    
    # Sign the message
    signature = schnorr_sign(message, p, g, private_key)
    
    # Save signature to file
    sig_file = "schnorr_signature.txt"
    with open(sig_file, 'w') as f:
        f.write(f"e = {signature[0]}\n")
        f.write(f"s = {signature[1]}\n")
    print(f"Signature saved to {sig_file}")
    
    # Verify the signature
    is_valid = schnorr_verify(message, signature, p, g, public_key)
    print(f"Signature verification result: {is_valid}")

if __name__ == "__main__":
    main()
