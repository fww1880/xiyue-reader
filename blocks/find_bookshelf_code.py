import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找书架相关代码
import re
matches = re.findall(r'.{0,50}(bookshelf|书架|QTreeWidget|customContextMenuRequested).{0,50}', content)
print("找到相关代码片段：")
seen = set()
for m in matches:
    if m not in seen:
        print(m)
        seen.add(m)