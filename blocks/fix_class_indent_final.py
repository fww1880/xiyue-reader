import os
import ast
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]
# 修复 class 内部所有方法的缩进：去掉多余的一级缩进
fixed_lines = []
inside_class = False
class_indent_fixed = False
for line in lines:
    if line.strip().startswith('class '):
        inside_class = True
        fixed_lines.append(line)
        continue
    if inside_class and not class_indent_fixed and line.strip():
        # class 内第一个方法，当前缩进是 8 个空格（class 顶格，方法应该缩进 4 个，现在多了一级）
        # 去掉一级缩进（4个空格）
        if line.startswith('        ') and len(line) > 8:
            # 从第 4 个字符开始（去掉 4 个空格）
            fixed_line = line[4:]
            fixed_lines.append(fixed_line)
            print(f"🔧 修复方法缩进：{line[:20]}... -> {fixed_line[:20]}...")
        else:
            fixed_lines.append(line)
        # 我们只需要修复第一个方法，后续所有行会自然继承缩进
        class_indent_fixed = True
    else:
        fixed_lines.append(line)
# 保存
content_final = '\n'.join(fixed_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content_final)
# 语法检查
try:
    ast.parse(content_final)
    print("\n✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"\n❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    lines_err = content_final.split('\n')
    start = max(0, e.lineno - 10)
    end = min(len(lines_err), e.lineno + 10)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
# 统计
print(f"\n📊 最终状态：")
print(f"   resource_path 定义：{content_final.count('def resource_path')}")
print(f"   import sys：{content_final.count('import sys')}")
print(f"   import os：{content_final.count('import os')}")