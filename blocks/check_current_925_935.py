import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 当前 L925-L935 内容：")
for i in range(924, min(935, len(lines))):
    line = lines[i]
    leading = len(line) - len(line.lstrip())
    print(f"L{i+1}: leading={leading:2d} | {repr(line.rstrip())}")