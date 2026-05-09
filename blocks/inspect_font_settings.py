import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 查找现有字体设置相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'font' in line.lower() and ('set' in line.lower() or 'action' in line or 'dialog' in line):
        print(f"  L{i}: {line.rstrip()}")
print()
# 查找字号默认值
print("=" * 60)
print("🔍 查找字号默认值：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'font_size' in line and 'self.settings.value' in line:
        print(f"  L{i}: {line.rstrip()}")
print()
# 查找字体设置方法
print("=" * 60)
print("🔍 查找字体设置方法：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def ' in line and 'font' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+30)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()