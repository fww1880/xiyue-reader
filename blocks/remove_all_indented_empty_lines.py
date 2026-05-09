import os
import re
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 删除所有有缩进的空行（如 '        '）
content = re.sub(r'        \n(?=\s*\n)', '\n', content)
print("✅ 已删除所有有缩进的空行")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)