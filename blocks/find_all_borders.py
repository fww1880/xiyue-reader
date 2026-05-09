import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找所有 border 相关的样式
import re
print("🔍 查找所有 border 相关设置：")
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'border' in line.lower() and ('#' in line or 'black' in line.lower() or '000' in line):
        # 检查是否是深色边框
        if '#000' in line or '#111' in line or '#222' in line or '#333' in line:
            print(f"  ❌ L{i}: {line.strip()}")
        else:
            print(f"  ✓ L{i}: {line.strip()}")
# 查找列表框样式（书签和目录）
print("\n🔍 查找书签和目录列表框样式：")
for i, line in enumerate(lines, 1):
    if 'toc_list' in line or 'bm_list_widget' in line:
        print(f"  L{i}: {line.strip()}")
        # 检查这附近有没有 setStyleSheet
        for j in range(i, min(i+10, len(lines))):
            if 'setStyleSheet' in lines[j]:
                print(f"    👉 找到样式设置：L{j+1}")
                break