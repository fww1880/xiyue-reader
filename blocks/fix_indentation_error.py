import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到错误位置附近
lines = content.split('\n')
print(f"总行数：{len(lines)}")
# 检查 1185-1190 行
print("\n🔍 检查错误位置（1185-1190 行）:")
for i in range(1180, min(1195, len(lines))):
    print(f"{i+1:4d}: {lines[i]}")
# 找到 add_bookmark 函数的位置
print("\n🔍 查找 add_bookmark 函数位置:")
for i, line in enumerate(lines):
    if 'def add_bookmark' in line:
        print(f"第 {i+1} 行：{line}")
        # 显示前后 10 行
        start = max(0, i-3)
        end = min(len(lines), i+30)
        print("上下文:")
        for j in range(start, end):
            marker = ">>> " if j == i else "    "
            print(f"{marker}{j+1:4d}: {lines[j]}")
        break
# 找到 get_position_preview 函数的位置
print("\n\n🔍 查找 get_position_preview 函数位置:")
for i, line in enumerate(lines):
    if 'def get_position_preview' in line:
        print(f"第 {i+1} 行：{line}")
        start = max(0, i-3)
        end = min(len(lines), i+20)
        print("上下文:")
        for j in range(start, end):
            marker = ">>> " if j == i else "    "
            print(f"{marker}{j+1:4d}: {lines[j]}")
        break