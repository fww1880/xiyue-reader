import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找 about_action 的 triggered 连接
print("🔍 查找 about_action 绑定：")
for i, line in enumerate(lines, 1):
    if 'about_action' in line:
        print(f"  L{i}: {line.rstrip()}")
# 找 show_about 或 about 方法
print("\n🔍 查找 show_about 方法：")
for i, line in enumerate(lines, 1):
    if 'def show_about' in line or 'def about' in line:
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+15)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()