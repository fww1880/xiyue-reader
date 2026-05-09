import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 直接替换两个空行为一个空行
content = content.replace('        \n        \n    def show_bookmark_list', '        \n    def show_bookmark_list')
print("✅ 已修复空行缩进")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)