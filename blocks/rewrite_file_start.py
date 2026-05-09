import os
from io import StringIO
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    original_content = f.read()
# 直接读取所有行，找到第一个 class，然后从头开始重新构建
lines = [line.rstrip('\n') for line in StringIO(original_content)]
# 把开头所有行都移出来，找到第一个 class
original_imports = []
first_class_line = None
for i, line in enumerate(lines):
    if line.strip().startswith('class '):
        first_class_line = i
        break
    original_imports.append(line)
# 构建新的开头：原 import + 干净的 resource_path + 原 class
new_start = []
# 添加原始 imports 去掉空行和重复
added_imports = set()
for line in original_imports:
    stripped = line.strip()
    if stripped in ('import sys', 'import os'):
        if stripped not in added_imports:
            new_start.append(line)
            added_imports.add(stripped)
    elif stripped:
        new_start.append(line)
# 添加干净的 resource_path（完全顶格）
new_start.append('')
new_start.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
new_start.append('def resource_path(relative_path):')
new_start.append('    try:')
new_start.append('        base_path = sys._MEIPASS')
new_start.append('    except AttributeError:')
new_start.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
new_start.append('    return os.path.join(base_path, relative_path)')
new_start.append('')
# 添加后面的内容从 first_class_line 开始
new_lines = new_start + lines[first_class_line:]
# 保存新文件
new_content = '\n'.join(new_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ 文件开头已重写，resource_path 缩进正确")
# 语法检查
import ast
try:
    tree = ast.parse(new_content)
    print("✅ Python 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
# 验证
print(f"\n📋 最终状态：")
print(f"  总行数：{len(new_lines)}")
print(f"  resource_path 定义：{new_content.count('def resource_path')}")
print(f"  import sys：{new_content.count('import sys')}")
print(f"  import os：{new_content.count('import os')}")
# 输出前 30 行看看
print("\n📄 前 30 行预览：")
for i, line in enumerate(new_lines[:30]):
    print(f" {i+1:2d}: {repr(line)}")