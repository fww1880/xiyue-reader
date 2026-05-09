import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 在第3行（from PyQt5.QtWidgets import）添加 QLabel 和 QListWidget
for i, line in enumerate(lines):
    if line.strip().startswith('from PyQt5.QtWidgets import'):
        # 检查括号内的内容
        if 'QLabel' not in line:
            # 在括号内添加
            if line.endswith(')'):
                line = line[:-1] + ', QLabel, QListWidget)'
            else:
                line = line.replace(')', ', QLabel, QListWidget)')
            lines[i] = line
            print("✅ 已在导入中添加 QLabel 和 QListWidget")
            break
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("🚀 导入修复完成！")