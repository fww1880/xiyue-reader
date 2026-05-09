import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 检查 1180-1200 行
print("🔍 检查 1180-1200 行:")
for i in range(1175, min(1205, len(lines))):
    line_content = lines[i].rstrip('\n')
    # 显示缩进字符
    indent_repr = repr(line_content[:20])
    print(f"{i+1:4d}: {line_content}")
    if i+1 == 1185 or i+1 == 1186:
        print(f"      ↑ 缩进表示：{indent_repr}")
# 查找 get_position_preview 函数定义
print("\n🔍 查找 get_position_preview 函数:")
for i, line in enumerate(lines):
    if 'def get_position_preview' in line:
        print(f"\n第 {i+1} 行：{line.rstrip()}")
        # 显示前后 10 行
        start = max(0, i-2)
        end = min(len(lines), i+15)
        for j in range(start, end):
            marker = ">>> " if j == i else "    "
            print(f"{marker}{j+1:4d}: {lines[j].rstrip()}")
        break