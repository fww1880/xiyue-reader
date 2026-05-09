import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'def load_book(self, file_path):' in line:
        for j in range(i, min(i+80, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
            if lines[j].strip().startswith('def ') and j > i:
                break