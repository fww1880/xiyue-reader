import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 show_bookshelf_context_menu 和 import_folder_to_bookshelf 方法
for i, line in enumerate(lines):
    if any(x in line for x in ['show_bookshelf_context_menu', 'import_folder_to_bookshelf', 'def open_file_dialog']):
        start = max(0, i-1)
        end = min(len(lines), i+30)
        print(f"--- Line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        print("-" * 40)