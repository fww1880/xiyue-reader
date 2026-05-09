import os
import ast
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]
# 从头开始整理，在第一个class之前插入干净的resource_path
clean_lines = []
inserted_rp = False
first_class_done = False
for line in lines:
    stripped = line.strip()
    # 遇到第一个class定义之前，插入resource_path
    if not inserted_rp and not first_class_done and stripped.startswith('class '):
        # 插入resource_path
        clean_lines.append('')
        clean_lines.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
        clean_lines.append('def resource_path(relative_path):')
        clean_lines.append('    try:')
        clean_lines.append('        base_path = sys._MEIPASS')
        clean_lines.append('    except AttributeError:')
        clean_lines.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
        clean_lines.append('    return os.path.join(base_path, relative_path)')
        clean_lines.append('')
        inserted_rp = True
        first_class_done = True
    # 跳过所有已存在的resource_path定义和注释
    if stripped.startswith('def resource_path') or '# 定义资源路径' in stripped:
        if inserted_rp:
            continue
    # 正常添加行
    clean_lines.append(line)
# 保存
final_content = '\n'.join(clean_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(final_content)
# 语法检查
try:
    ast.parse(final_content)
    print("✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    lines_err = final_content.split('\n')
    start = max(0, e.lineno - 5)
    end = min(len(lines_err), e.lineno + 5)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
# 统计
print(f"\n📊 最终统计：")
print(f"   resource_path 定义：{final_content.count('def resource_path')}")
print(f"   总行数：{len(clean_lines)}")