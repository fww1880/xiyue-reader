import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'novel_reader'))
# 查看目录结构
reader_dir = os.path.join(os.getcwd(), 'novel_reader')
for root, dirs, files in os.walk(reader_dir):
    level = root.replace(reader_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')