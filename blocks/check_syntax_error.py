import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"🔍 检查第 470-500 行代码 (当前文件共 {len(lines)} 行)...")
for i in range(469, min(510, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")