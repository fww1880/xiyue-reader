import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
print("🔍 检查窗口初始化代码：")
in_init = False
for i, line in enumerate(lines, 1):
    if 'def __init__' in line:
        in_init = True
    if in_init:
        print(f"L{i}: {line.strip()}")
        if i > 50 and 'def ' in line and '__init__' not in line:
            break