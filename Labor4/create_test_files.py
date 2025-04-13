import os
import random

def create_binary_file(filename: str, size_mb: int):
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

if __name__ == "__main__":
    sizes = [1, 5, 10]  # MB
    for i, size in enumerate(sizes, 1):
        create_binary_file(f"test{i}.bin", size) 