import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找包含 setMinimumSize, setMaximumSize, setFixedSize, resize 的行及其上下文
for i, line in enumerate(lines):
    if any(kw in line for kw in ['setMinimumSize', 'setMaximumSize', 'setFixedSize', 'resize']):
        print(f"Line {i+1}: {line.strip()}")
        # 打印上下文
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 40)