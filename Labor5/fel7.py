#7. Hasonlítsuk össze a Salsa20 és AES-256 titkosítók időigényét.
import time
import os
from Crypto.Cipher import Salsa20, AES

def measure_salsa20(data_size, iterations=100):
    total_time = 0
    for _ in range(iterations):
        key = os.urandom(32)
        nonce = os.urandom(8)
        data = os.urandom(data_size)
        
        start_time = time.time()
        cipher = Salsa20.new(key=key, nonce=nonce)
        encrypted = cipher.encrypt(data)
        end_time = time.time()
        
        total_time += (end_time - start_time)
    
    return total_time / iterations

def measure_aes256(data_size, iterations=100):
    total_time = 0
    for _ in range(iterations):
        key = os.urandom(32)
        iv = os.urandom(16)
        data = os.urandom(data_size)
        
        start_time = time.time()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Pad data to be multiple of 16 bytes
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length]) * padding_length
        encrypted = cipher.encrypt(padded_data)
        end_time = time.time()
        
        total_time += (end_time - start_time)
    
    return total_time / iterations

def compare_algorithms():
    data_sizes = [1024, 10240, 102400, 1024000]  # Different data sizes in bytes
    iterations = 100
    
    print("Comparing Salsa20 and AES-256 encryption performance")
    print("-" * 50)
    print(f"{'Data Size (bytes)':20} {'Salsa20 (ms)':15} {'AES-256 (ms)':15} {'Ratio (AES/Salsa)':20}")
    print("-" * 50)
    
    for size in data_sizes:
        salsa_time = measure_salsa20(size, iterations) * 1000  # Convert to ms
        aes_time = measure_aes256(size, iterations) * 1000  # Convert to ms
        ratio = aes_time / salsa_time if salsa_time > 0 else 0
        
        print(f"{size:20} {salsa_time:.6f}ms {aes_time:.6f}ms {ratio:.6f}")
    
    print("-" * 50)

if __name__ == "__main__":
    compare_algorithms()
