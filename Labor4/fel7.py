from base64 import b64decode
from Crypto.Cipher import ChaCha20_Poly1305

def verify_authenticity():
    with open('poly1305.txt', 'r') as file:
        lines = file.readlines()
        
    for i in range(0, len(lines), 4):
        if i + 3 >= len(lines):
            break
            
        key = b64decode(lines[i].strip())
        nonce = b64decode(lines[i+1].strip())
        ciphertext = b64decode(lines[i+2].strip())
        tag = b64decode(lines[i+3].strip())
        
        try:
            cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
            cipher.decrypt_and_verify(ciphertext, tag)
            print(f"Message {i//4 + 1}: Authentic")
        except (ValueError, KeyError):
            print(f"Message {i//4 + 1}: Not authentic")

if __name__ == "__main__":
    verify_authenticity()
