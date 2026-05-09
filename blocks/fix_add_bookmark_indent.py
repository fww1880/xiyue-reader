import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 修复 L904 的缩进：从 leading=0 改为 leading=4
lines[903] = '    def add_bookmark(self):\n'
# 删除 L927-L929（leading=1 的空行）
del lines[926:929]
# 删除 L930-L931（孤立的代码）
del lines[926:928]
print("✅ 已修复 add_bookmark 缩进并删除孤立代码")
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)