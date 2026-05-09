import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]
# 删除所有以 "# 定义资源路径处理函数" 开头但在 resource_path 定义之后的行
clean_lines = []
found_rp_def = False
for line in lines:
    if '# 定义资源路径处理函数' in line and found_rp_def:
        print(f"🗑️  删除重复注释行：{line}")
        continue
    if 'def resource_path' in line:
        found_rp_def = True
    clean_lines.append(line)
# 确保只有一个 resource_path 定义
found_rp = False
final_lines = []
for line in clean_lines:
    if 'def resource_path' in line:
        if found_rp:
            print(f"🗑️  删除重复的 resource_path 定义行：{line}")
            continue
        found_rp = True
    final_lines.append(line)
# 保存
content = '\n'.join(final_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 重复行已删除")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    # 输出出错行附近
    lines_err = content.split('\n')
    start = max(0, e.lineno - 5)
    end = min(len(lines_err), e.lineno + 5)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
# 统计
print(f"\n📊 最终统计：")
print(f"   resource_path 定义：{content.count('def resource_path')}")
print(f"   import sys：{content.count('import sys')}")
print(f"   import os：{content.count('import os')}")