import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 查找翻页/上下页相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'prev' in line.lower() or 'next' in line.lower() or '上页' in line or '下页' in line or 'page' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找动画相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'animation' in line.lower() or 'QPropertyAnimation' in line or 'QParallelAnimationGroup' in line:
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找翻页方法定义：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def prev' in line.lower() or 'def next' in line.lower() or 'def page' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+15)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()