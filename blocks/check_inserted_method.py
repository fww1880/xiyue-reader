import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 检查 get_position_preview 方法...")
for i in range(900, 940):
    if 'get_position_preview' in lines[i]:
        print(f"L{i+1}: {lines[i].rstrip()}")
# 查看完整方法
start = None
for i, line in enumerate(lines):
    if 'def get_position_preview' in line:
        start = i
        break
if start:
    end = start
    while end < len(lines) and (lines[end].startswith('    ') or lines[end].strip() == ''):
        end += 1
    print(f"\n完整方法（L{start+1}-L{end}）：")
    for i in range(start, end):
        print(f"L{i+1}: {lines[i].rstrip()}")