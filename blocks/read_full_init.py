import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 打印 __init__ 方法的前 50 行
start_idx = 0
for i, line in enumerate(lines):
    if 'def __init__(self' in line:
        start_idx = i
        break
for i in range(start_idx, min(start_idx + 60, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")