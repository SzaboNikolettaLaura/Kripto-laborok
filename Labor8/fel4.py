from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

# Generate a 2048 bit RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# Save private key to file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save public key to file
with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# File to sign (create a sample file if it doesn't exist)
file_to_sign = "sample.bin"
if not os.path.exists(file_to_sign):
    with open(file_to_sign, "wb") as f:
        f.write(os.urandom(64))  # Create a 64-byte random binary file

# Read the file content
with open(file_to_sign, "rb") as f:
    message = f.read()

# Create a digital signature
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Save the signature to a file
with open("signature.bin", "wb") as f:
    f.write(signature)

# Verify the signature
try:
    # Load the public key from file to demonstrate reading the keys
    with open("public_key.pem", "rb") as f:
        loaded_public_key = serialization.load_pem_public_key(f.read())
    
    # Verify signature
    loaded_public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature verified successfully.")
except Exception as e:
    print(f"Signature verification failed: {e}")
