import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找并修复缩进错误
fixed_lines = []
for i, line in enumerate(lines):
    if 'class NovelReaderMainWindow(QMainWindow):    def keyboard_pagination' in line:
        # 这行坏了，拆分成两行
        fixed_lines.append('class NovelReaderMainWindow(QMainWindow):\n')
        fixed_lines.append('    def keyboard_pagination(self, event):\n')
    else:
        fixed_lines.append(line)
# 写入修复后的文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)
print("✅ 缩进错误已修复！")
# 再次检查语法
import ast
try:
    with open(main_file, 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 仍然有语法错误：第 {e.lineno} 行")
    print(e.text)