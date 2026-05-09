import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找书架相关代码
for i, line in enumerate(lines):
    if 'bookshelf' in line.lower() or '书架' in line or 'contextMenu' in line or 'customContextMenu' in line:
        start = max(0, i-2)
        end = min(len(lines), i+15)
        print(f"--- Line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        print("-" * 40)