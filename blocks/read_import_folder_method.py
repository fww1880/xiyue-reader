import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找 import_folder_to_bookshelf 或导入相关方法
for i, line in enumerate(lines):
    if 'def import' in line.lower() or 'def add_to' in line.lower() or 'def add_book' in line.lower():
        start = max(0, i-1)
        end = min(len(lines), i+30)
        print(f"--- Line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        print("-" * 40)