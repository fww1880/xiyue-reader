import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 检查书架布局代码是否有缺失导入...")
# 检查 QLabel 和 QListWidget 是否导入
import_lines = []
for i, line in enumerate(lines):
    if 'from PyQt5' in line or 'import' in line and 'PyQt5' in line:
        import_lines.append(f"L{i+1}: {line.strip()}")
print("导入语句：")
for imp in import_lines[:10]:
    print(imp)
# 检查 QLabel 是否在导入中
has_qlabel = False
has_qlistwidget = False
for line in lines:
    if 'QLabel' in line and 'from PyQt5' in line:
        has_qlabel = True
    if 'QListWidget' in line and 'from PyQt5' in line:
        has_qlistwidget = True
if not has_qlabel:
    print("⚠️ 可能缺少 QLabel 导入")
if not has_qlistwidget:
    print("⚠️ 可能缺少 QListWidget 导入")
# 检查书架布局代码附近是否有导入
for i in range(240, 260):
    if 'QLabel' in lines[i] or 'QListWidget' in lines[i]:
        print(f"L{i+1} 使用了控件：{lines[i].strip()}")