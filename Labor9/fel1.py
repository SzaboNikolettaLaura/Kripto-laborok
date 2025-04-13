import json
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from base64 import b16decode

# 1. Digitális aláírás ellenőrzése
def verify_signature(public_key_to_verify_path, ca_public_key_path, signatures_path):
    # Betöltjük a CA publikus kulcsot (aláírás ellenőrzéshez)
    with open(ca_public_key_path, 'rb') as f:
        ca_public_key = ed25519.Ed25519PublicKey.from_public_bytes(
            serialization.load_pem_public_key(f.read(), backend=default_backend()).public_bytes(
                serialization.Encoding.Raw, serialization.PublicFormat.Raw
            )
        )

    # Betöltjük a signatures JSON-t
    with open(signatures_path, 'r') as f:
        signatures = json.load(f)

    # Betöltjük az ellenőrizendő publikus kulcsot
    with open(public_key_to_verify_path, 'rb') as f:
        public_key_bytes = serialization.load_pem_public_key(f.read(), backend=default_backend()).public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )

    # Létrehozzuk a SHA512 hash-t a nyers publikus kulcsról
    hash_value = hashlib.sha512(public_key_bytes).digest()

    found = False
    for record in signatures:
        name = record['name']
        signature_hex = record['signature']
        signature_bytes = b16decode(signature_hex.encode(), casefold=True)
        try:
            ca_public_key.verify(signature_bytes, hash_value)
            print(f"A kulcs {name} aláírásával hitelesítve.")
            found = True
        except Exception:
            continue

    if not found:
        print("A kulcs nem található a hitelesített aláírások között.")

# 2. Diffie-Hellman ECC kulcsmegosztás és 32 byte-os titkos kulcs létrehozása
def ecc_key_exchange(private_key_path, password):
    # ECC kulcs betöltése - az EC kulcs támogatja a key exchange-et
    with open(private_key_path, 'rb') as f:
        try:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=password.encode() if password else None,
                backend=default_backend()
            )
            
            # Ellenőrizzük, hogy EC típusú-e a kulcs
            if not isinstance(private_key, ec.EllipticCurvePrivateKey):
                # Ha nem EC kulcs, generáljunk egy újat
                print("A megadott kulcs nem EC típusú, új EC kulcs generálása...")
                private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
        except Exception as e:
            print(f"Hiba a kulcs betöltésekor: {e}")
            print("Új EC kulcs generálása...")
            private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())

    # Létrehozunk egy ideiglenes partner publikus kulcsot
    peer_private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
    peer_public_key = peer_private_key.public_key()

    # Létrehozzuk a megosztott kulcsot
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

    # A megosztott kulcsból leszűrünk egy 32 byte-os kulcsot HKDF-fel
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)

    print("Létrehozott 32 byte-os titkos kulcs (hex):", derived_key.hex())

if __name__ == "__main__":
    # Fájlnevek megadása
    public_key_to_verify_path = "publicKeyECC_B_9_1.pem"
    ca_public_key_path = "publicKeyECC_CA_9_1.pem"
    signatures_path = "signatures9_1.json"
    private_key_path = "privateKeyECC_A_9_1.pem"
    password = "pasword_A_9_1"

    print("1. Digitális aláírás ellenőrzése:")
    verify_signature(public_key_to_verify_path, ca_public_key_path, signatures_path)

    print("\n2. ECC kulcsmegosztás és 32 byte-os titkos kulcs generálás:")
    ecc_key_exchange(private_key_path, password)
