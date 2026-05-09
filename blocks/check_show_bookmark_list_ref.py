import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 L460-L480 上下文：")
for i in range(459, min(480, len(lines))):
    line = lines[i]
    leading = len(line) - len(line.lstrip())
    print(f"L{i+1}: leading={leading:2d} | {repr(line.rstrip())}")