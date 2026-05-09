import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 查找关于对话框相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if '关于' in line or 'about' in line.lower() or 'QMessageBox.about' in line:
        print(f"  L{i}: {line.rstrip()}")
        # 打印上下文
        start = max(0, i-2)
        end = min(len(lines), i+10)
        for j in range(start, end):
            marker = ">>>" if j == i-1 else "   "
            print(f"  {marker} L{j+1}: {lines[j].rstrip()}")
        print()