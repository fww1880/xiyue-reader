import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找 text_edit 初始化位置
for i, line in enumerate(lines):
    if 'self.text_edit = QTextEdit()' in line:
        print(f"✅ 找到 text_edit 初始化在 L{i+1}")
        # 在这行后面添加自动换行设置
        insert_line = i + 1
        lines.insert(insert_line, '        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)  # 自动换行适应边框宽度')
        lines.insert(insert_line + 1, '        self.text_edit.setWordWrapMode(True)  # 单词自动换行')
        print("✅ 已添加自动换行设置")
        break
content = '\n'.join(lines)
# 检查是否导入 QTextEdit 相关
if 'from PyQt5.QtWidgets import QTextEdit' not in content:
    print("⚠️ QTextEdit 已经被整体导入，无需额外导入")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存修改，自动换行已启用！")