import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找所有包含 QMessageBox.question 的行
print("=" * 60)
print("🔍 查找所有 QMessageBox.question 出现位置：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'QMessageBox.question' in line:
        print(f"  L{i}: {line.rstrip()}")
        # 打印上下文
        start = max(0, i-3)
        end = min(len(lines), i+6)
        print(f"  --- 上下文 (L{start+1}-L{end}) ---")
        for j in range(start, end):
            marker = ">>>" if j == i-1 else "   "
            print(f"  {marker} L{j+1}: {lines[j].rstrip()}")
        print()
# 查找 toggle_bookmark 或快捷键处理中调用 add_bookmark 的代码
print("=" * 60)
print("🔍 查找 toggle_bookmark 方法：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def toggle_bookmark' in line:
        print(f"  L{i}: {line.rstrip()}")
        # 打印整个方法
        for j in range(i, min(len(lines), i+30)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()
# 查找快捷键绑定
print("=" * 60)
print("🔍 查找快捷键 Ctrl+D 绑定：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'Ctrl+D' in line or 'Control+D' in line or 'Qt.Key_D' in line:
        print(f"  L{i}: {line.rstrip()}")
        start = max(0, i-2)
        end = min(len(lines), i+5)
        for j in range(start, end):
            marker = ">>>" if j == i-1 else "   "
            print(f"  {marker} L{j+1}: {lines[j].rstrip()}")
        print()
# 查找书签位置相关代码
print("=" * 60)
print("🔍 查找书签位置保存逻辑（add_bookmark 方法）：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def add_bookmark' in line:
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+40)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()
# 查找书签跳转逻辑
print("=" * 60)
print("🔍 查找书签跳转逻辑（jump_to_bookmark 或类似方法）：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def jump' in line.lower() and 'bookmark' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+30)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()