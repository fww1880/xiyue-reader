import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 查找工具栏按钮相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'toolbar' in line.lower() or 'QAction' in line or 'addAction' in line or 'setShortcut' in line:
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找滚屏/滚动相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'scroll' in line.lower() or '滚屏' in line or 'auto' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找 QTimer 相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'QTimer' in line or 'timer' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找 __init__ 方法中的初始化代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def __init__' in line:
        for j in range(i, min(len(lines), i+30)):
            print(f"  L{j+1}: {lines[j].rstrip()}")
        break