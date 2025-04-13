import time
import numpy as np

class A51:
    def __init__(self, key):
        self.key = key
        self.reg1 = [0] * 19
        self.reg2 = [0] * 22
        self.reg3 = [0] * 23
        
        # Initialize registers with key
        for i in range(64):
            bit = (key >> i) & 1
            self.reg1[0] = bit
            self.reg2[0] = bit
            self.reg3[0] = bit
            self._clock_all()
    
    def _clock(self, reg, size, tap1, tap2):
        feedback = reg[tap1] ^ reg[tap2]
        reg.pop()
        reg.insert(0, feedback)
        return reg[0]
    
    def _clock_all(self):
        # Clock each register
        bit1 = self._clock(self.reg1, 19, 8, 13)
        bit2 = self._clock(self.reg2, 22, 10, 20)
        bit3 = self._clock(self.reg3, 23, 10, 21)
        
        # Majority function
        majority = (bit1 & bit2) ^ (bit1 & bit3) ^ (bit2 & bit3)
        
        # Clock registers based on majority
        if bit1 == majority:
            self._clock(self.reg1, 19, 8, 13)
        if bit2 == majority:
            self._clock(self.reg2, 22, 10, 20)
        if bit3 == majority:
            self._clock(self.reg3, 23, 10, 21)
    
    def get_next_bit(self):
        self._clock_all()
        return self.reg1[0] ^ self.reg2[0] ^ self.reg3[0]

def encrypt_file(input_file, output_file, key):
    start_time = time.time()
    
    a51 = A51(key)
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            byte = f_in.read(1)
            if not byte:
                break
            encrypted_byte = 0
            for i in range(8):
                encrypted_byte |= (a51.get_next_bit() << i)
            f_out.write(bytes([encrypted_byte ^ byte[0]]))
    
    return time.time() - start_time

def decrypt_file(input_file, output_file, key):
    # Decryption is the same as encryption
    return encrypt_file(input_file, output_file, key)

def test_performance(file_sizes):
    key = 0x1234567890ABCDEF
    results = []
    
    for size in file_sizes:
        # Create test file
        test_data = np.random.bytes(size)
        with open('test.bin', 'wb') as f:
            f.write(test_data)
        
        # Measure encryption
        enc_time = encrypt_file('test.bin', 'encrypted.bin', key)
        
        # Measure decryption
        dec_time = decrypt_file('encrypted.bin', 'decrypted.bin', key)
        
        results.append((size, enc_time, dec_time))
        
        # Clean up
        import os
        os.remove('test.bin')
        os.remove('encrypted.bin')
        os.remove('decrypted.bin')
    
    return results

if __name__ == "__main__":
    # Test with different file sizes
    file_sizes = [1024, 10240, 102400, 1024000]  # 1KB, 10KB, 100KB, 1MB
    results = test_performance(file_sizes)
    
    print("File Size\tEncryption Time\tDecryption Time")
    print("--------------------------------------------")
    for size, enc_time, dec_time in results:
        print(f"{size/1024:.1f} KB\t{enc_time:.4f} s\t{dec_time:.4f} s")
