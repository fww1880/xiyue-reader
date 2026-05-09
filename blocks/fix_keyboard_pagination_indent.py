import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]
# 找到第 26-35 行，修复缩进
fixed_lines = []
# 我们重新修复前 40 行，确保缩进正确
for i, line in enumerate(lines):
    if 24 <= i <= 29:  # 从 keyboard_pagination 开始
        if line.strip() == '':
            # 空行也要保持缩进
            fixed_lines.append('        ')
        elif line.strip():
            # 函数体内需要缩进 8 个空格（两个级别：类 + 方法）
            if not line.startswith('        ') and line.strip():
                fixed_lines.append('        ' + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    elif i == 30 and 'import sys' in line:
        # 这行不应该在这里，说明我们插入 resource_path 的位置错了
        # 跳过这一段，因为 resource_path 已经在前面了
        # 我们需要找到从哪里开始是原来的 keyboard_pagination 继续
        # 重新扫描：找到 class NovelReaderMainWindow 之后第一个 def 就是 __init__ 或 keyboard...
        print(f"⚠️ 发现错误插入位置，重新整理...")
        break
    else:
        fixed_lines.append(line)
# 现在重新来：找到正确的插入位置
# 从头开始找：找第一个 class 定义，在 class 之前插入 resource_path
lines = [line.rstrip('\n') for line in open(main_file, 'r', encoding='utf-8')]
clean_lines = []
inserted = False
first_class_found = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if not first_class_found and stripped.startswith('class '):
        # 在第一个 class 之前插入 resource_path
        clean_lines.append('')
        clean_lines.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
        clean_lines.append('def resource_path(relative_path):')
        clean_lines.append('    try:')
        clean_lines.append('        base_path = sys._MEIPASS')
        clean_lines.append('    except AttributeError:')
        clean_lines.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
        clean_lines.append('    return os.path.join(base_path, relative_path)')
        clean_lines.append('')
        first_class_found = True
        inserted = True
    # 删除所有已经存在的 resource_path 定义
    if 'def resource_path' in line and inserted:
        # 跳过这个定义，因为已经插入了
        # 继续跳过整个函数
        continue
    if '# 定义资源路径' in line and inserted:
        continue
    clean_lines.append(line)
# 现在检查缩进
final_content = '\n'.join(clean_lines)
import ast
try:
    ast.parse(final_content)
    print("✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 在第 {e.lineno} 行")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(final_content)
print("\n📊 最终状态：")
print(f"  resource_path 定义：{final_content.count('def resource_path')}")
print(f"  总行数：{len(clean_lines)}")