import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 toggle_auto_scroll 的精确代码
print("🔍 查找 toggle_auto_scroll 精确代码：")
for i, line in enumerate(lines, 1):
    if 'def toggle_auto_scroll' in line:
        for j in range(i, min(len(lines), i+12)):
            print(f"  L{j+1}: {repr(lines[j])}")
        break