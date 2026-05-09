import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("🔍 搜索所有书签相关方法：")
import re
methods = re.findall(r'def (\w*bookmark\w*)\(', content)
for method in methods:
    print(f"  - {method}")