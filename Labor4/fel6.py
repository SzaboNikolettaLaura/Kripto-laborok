import time
import sys

class LFSR16:
    def __init__(self, key):
        self.state = key & 0xFFFF
        self.taps = 0xB400  # x^16 + x^14 + x^13 + x^11 + 1

    def next_bit(self):
        feedback = 0
        for i in range(16):
            if (self.taps >> i) & 1:
                feedback ^= (self.state >> i) & 1
        self.state = ((self.state << 1) | feedback) & 0xFFFF
        return feedback

    def generate_byte(self):
        byte = 0
        for i in range(8):
            byte = (byte << 1) | self.next_bit()
        return byte

def read_key_from_file(filename):
    with open(filename, 'r') as f:
        key_hex = f.read().strip()
        return int(key_hex, 16)

def process_file(input_file, output_file, key_file, encrypt=True):
    key = read_key_from_file(key_file)
    lfsr = LFSR16(key)
    
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            byte = f_in.read(1)
            if not byte:
                break
            lfsr_byte = lfsr.generate_byte()
            result_byte = bytes([byte[0] ^ lfsr_byte])
            f_out.write(result_byte)

def main():
    if len(sys.argv) != 5:
        print("Usage: python fel6.py <input_file> <output_file> <key_file> <encrypt/decrypt>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key_file = sys.argv[3]
    mode = sys.argv[4].lower()

    if mode not in ['encrypt', 'decrypt']:
        print("Mode must be either 'encrypt' or 'decrypt'")
        return

    start_time = time.time()
    process_file(input_file, output_file, key_file, mode == 'encrypt')
    end_time = time.time()

    print(f"Processing time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
