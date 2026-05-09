import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 读取完整的 import_folder 方法
start = None
for i, line in enumerate(lines):
    if 'def import_folder(self):' in line:
        start = i
        break
if start:
    for i in range(start, min(start + 80, len(lines))):
        print(f"{i+1}: {lines[i].rstrip()}")
        if lines[i].strip().startswith('def ') and i > start:
            break