import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找工具栏相关代码
print("🔍 查找工具栏相关代码...")
for i, line in enumerate(lines):
    if 'toolbar' in line.lower() or 'QToolBar' in line:
        start = max(0, i-2)
        end = min(len(lines), i+8)
        for j in range(start, end):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        print("-" * 60)