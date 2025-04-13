import base64
import time
from typing import Tuple

class RC4:
    def __init__(self, key: bytes):
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def _prga(self) -> int:
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        return self.S[(self.S[self.i] + self.S[self.j]) % 256]

    def process(self, data: bytes) -> bytes:
        # Skip first 1024 bytes
        for _ in range(1024):
            self._prga()
        
        result = bytearray()
        for byte in data:
            result.append(byte ^ self._prga())
        return bytes(result)

def read_key(key_file: str) -> bytes:
    with open(key_file, 'r') as f:
        key_b64 = f.read().strip()
        return base64.b64decode(key_b64)

def process_file(input_file: str, output_file: str, key_file: str, encrypt: bool = True) -> Tuple[float, int]:
    key = read_key(key_file)
    rc4 = RC4(key)
    
    with open(input_file, 'rb') as f:
        data = f.read()
    
    start_time = time.time()
    processed_data = rc4.process(data)
    end_time = time.time()
    
    with open(output_file, 'wb') as f:
        f.write(processed_data)
    
    return end_time - start_time, len(data)

def main():
    key_file = "key.txt"
    test_files = ["test1.bin", "test2.bin", "test3.bin"]
    
    print("File Size (bytes)\tEncryption Time (s)\tDecryption Time (s)")
    print("-" * 60)
    
    for test_file in test_files:
        encrypted_file = f"encrypted_{test_file}"
        decrypted_file = f"decrypted_{test_file}"
        
        enc_time, file_size = process_file(test_file, encrypted_file, key_file, True)
        dec_time, _ = process_file(encrypted_file, decrypted_file, key_file, False)
        
        print(f"{file_size}\t\t{enc_time:.6f}\t\t{dec_time:.6f}")

if __name__ == "__main__":
    main()
