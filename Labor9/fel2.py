import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii

# Constants
PASSWORD = "CA_Password9_2"
INPUT_JSON = "pk9_2.json"
CA_PRIVATE_KEY = "privateKeyECC_CA_9_2.pem"
OUTPUT_JSON = "signed_servers_9_2.json"

def load_private_key(key_path, password):
    """Load the CA's private key from PEM file"""
    with open(key_path, "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=password.encode()
        )
    return private_key

def hex_to_bytes(hex_string):
    """Convert hexadecimal string to bytes"""
    return binascii.unhexlify(hex_string)

def create_signed_servers_json():
    # Load CA private key
    private_key = load_private_key(CA_PRIVATE_KEY, PASSWORD)
    
    # Load server data
    with open(INPUT_JSON, 'r') as f:
        servers = json.load(f)
    
    # Create new data with signatures
    signed_servers = []
    for server in servers:
        name = server["name"]
        public_key_hex = server["publicKey"]
        
        # Convert hex public key to bytes for signing
        public_key_bytes = hex_to_bytes(public_key_hex)
        
        # Sign the raw public key
        signature = private_key.sign(public_key_bytes)
        signature_hex = binascii.hexlify(signature).decode('ascii')
        
        # Add to signed servers list
        signed_servers.append({
            "name": name,
            "publicKey": public_key_hex,
            "signature": signature_hex
        })
    
    # Write to output file
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(signed_servers, f, indent=4)
    
    print(f"Created {OUTPUT_JSON} with {len(signed_servers)} signed server entries")

if __name__ == "__main__":
    create_signed_servers_json()
