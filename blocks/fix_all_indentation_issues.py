import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 修复第1400-1420行的缩进
print("🔧 修复第1400-1420行缩进...")
fixed_lines = []
for i, line in enumerate(lines):
    if i >= 1403 and i <= 1418:
        # 当前是8个空格，应该改为4个
        content = line.lstrip()
        if content:
            fixed_line = '    ' + content
            fixed_lines.append(fixed_line)
            print(f"第 {i+1} 行：{repr(line)} → {repr(fixed_line)}")
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)
content = ''.join(fixed_lines)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    # 显示错误位置
    lines = content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        print(f"{i+1:4d}: {repr(lines[i])}")