import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找 change_theme 方法
print("🔍 查找 change_theme 方法：")
in_method = False
method_lines = []
for i, line in enumerate(lines, 1):
    if 'def change_theme' in line:
        in_method = True
        print(f"\n✅ 找到方法定义 L{i}:")
    if in_method:
        print(f"L{i}: {line}")
        method_lines.append(line)
        # 方法结束判断
        if line.strip() and not line.startswith(' ') and not line.startswith('\t') and method_lines:
            break
        # 如果下一行是新的 def 或 class，也结束
        if i < len(lines) - 1 and (lines[i].startswith('def ') or lines[i].startswith('class ')):
            break