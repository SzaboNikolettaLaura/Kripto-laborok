import os
import glob

def collect_py_files():
    # Get all .py files from Labor1 to Labor9 folders
    all_py_files = []
    
    for i in range(1, 10):
        labor_dir = f"Labor{i}"
        if os.path.exists(labor_dir):
            py_files = glob.glob(f"{labor_dir}/*.py")
            all_py_files.extend(py_files)
    
    # Sort files by folder and name
    all_py_files.sort()
    
    # Create output file
    output_path = "all_python_files.txt"
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for py_file in all_py_files:
            folder_name = os.path.basename(os.path.dirname(py_file))
            file_name = os.path.basename(py_file)
            
            outfile.write(f"\n\n{'=' * 80}\n")
            outfile.write(f"File: {folder_name}/{file_name}\n")
            outfile.write(f"{'=' * 80}\n\n")
            
            try:
                with open(py_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
            except UnicodeDecodeError:
                try:
                    # Try with Latin-1 encoding if UTF-8 fails
                    with open(py_file, 'r', encoding='latin-1') as infile:
                        content = infile.read()
                        outfile.write(content)
                except Exception as e:
                    outfile.write(f"Error reading file: {e}\n")
    
    print(f"All Python files have been collected in {output_path}")

if __name__ == "__main__":
    collect_py_files() 