import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 删除第1405行的重复定义
fixed_lines = []
for i, line in enumerate(lines):
    if i == 1405 and 'def save_bookmarks' in line:
        print(f"🗑️ 删除重复行 {i+1}: {line}")
        continue
    fixed_lines.append(line)
content = ''.join(fixed_lines)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    lines = content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        print(f"{i+1:4d}: {repr(lines[i])}")