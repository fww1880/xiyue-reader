import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 refresh_bookmark_list 完整方法：")
start = None
for i, line in enumerate(lines):
    if 'def refresh_bookmark_list' in line:
        start = i
        break
if start:
    end = start
    while end < len(lines) and (lines[end].startswith('    ') or lines[end].strip() == ''):
        end += 1
    for i in range(start, end):
        print(f"L{i+1}: {lines[i].rstrip()}")