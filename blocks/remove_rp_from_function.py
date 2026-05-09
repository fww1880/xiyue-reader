import os
import ast
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]
# 找到 keyboard_pagination 函数，删除里面错误插入的 resource_path
clean_lines = []
inside_wrong_rp = False
current_indent = 0
rp_lines_count = 0
for line in lines:
    # 如果已经进入错误插入的 resource_path，继续跳过直到恢复正确缩进
    if inside_wrong_rp:
        rp_lines_count += 1
        # 当我们回到和函数定义一样的缩进，就结束错误区域
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent <= current_indent and stripped:
            inside_wrong_rp = False
            print(f"✂️  已删除错误插入的 {rp_lines_count} 行 resource_path 代码")
        else:
            continue
    # 检查是不是错误插入开始了
    if 'def resource_path(' in line and current_indent > 0:
        inside_wrong_rp = True
        current_indent = len(line) - len(line.lstrip())
        print(f"⚠️  发现错误插入的 resource_path 在函数内部，缩进 {current_indent}，开始删除...")
        continue
    clean_lines.append(line)
# 现在重新正确插入 resource_path 在第一个 class 之前
final_lines = []
inserted = False
for line in clean_lines:
    stripped = line.strip()
    if not inserted and stripped.startswith('class '):
        # 插入正确的 resource_path 在开头
        final_lines.append('')
        final_lines.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
        final_lines.append('def resource_path(relative_path):')
        final_lines.append('    try:')
        final_lines.append('        base_path = sys._MEIPASS')
        final_lines.append('    except AttributeError:')
        final_lines.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
        final_lines.append('    return os.path.join(base_path, relative_path)')
        final_lines.append('')
        inserted = True
    # 跳过其他重复的 resource_path
    if (stripped.startswith('def resource_path') or '# 定义资源路径' in stripped) and inserted:
        continue
    final_lines.append(line)
# 保存
final_content = '\n'.join(final_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(final_content)
# 语法检查
try:
    ast.parse(final_content)
    print("\n✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"\n❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    lines_err = final_content.split('\n')
    start = max(0, e.lineno - 10)
    end = min(len(lines_err), e.lineno + 10)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
# 统计
print(f"\n📊 最终状态：")
print(f"   resource_path 定义：{final_content.count('def resource_path')}")
print(f"   import sys：{final_content.count('import sys')}")
print(f"   import os：{final_content.count('import os')}")