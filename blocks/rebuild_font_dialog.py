import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 open_font_settings 的起始和结束行
start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'def open_font_settings' in line:
        start_line = i
        break
if start_line is None:
    print("❌ 未找到 open_font_settings 方法")
    exit()
print(f"✅ open_font_settings 从 L{start_line+1} 开始")
# 找到结束（下一个 def）
for j in range(start_line+1, len(lines)):
    stripped = lines[j].strip()
    if stripped.startswith('def ') or stripped.startswith('class '):
        end_line = j
        break
print(f"✅ 结束于 L{end_line+1}")
# 完整重写整个方法
new_method = [
'    def open_font_settings(self):',
'        """打开字体设置对话框"""',
'        from PyQt5.QtWidgets import QFontComboBox, QComboBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QDialogButtonBox',
'        dialog = QDialog(self)',
'        dialog.setWindowTitle("字体设置")',
'        dialog.resize(400, 300)',
'        layout = QVBoxLayout(dialog)',
'',
'        # 字体选择',
'        font_layout = QHBoxLayout()',
'        font_layout.addWidget(QLabel("字体:"))',
'        font_combo = QFontComboBox()',
'        current_font = self.text_edit.font()',
'        font_combo.setCurrentFont(current_font)',
'        font_layout.addWidget(font_combo)',
'        layout.addLayout(font_layout)',
'',
'        # 字号设置',
'        size_layout = QHBoxLayout()',
'        size_layout.addWidget(QLabel("字号:"))',
'        size_spin = QSpinBox()',
'        size_spin.setValue(current_font.pointSize())',
'        size_spin.setRange(8, 48)',
'        size_layout.addWidget(size_spin)',
'        layout.addLayout(size_layout)',
'',
'        # 行高设置',
'        line_height_layout = QHBoxLayout()',
'        line_height_layout.addWidget(QLabel("行高:"))',
'        line_height_spin = QDoubleSpinBox()',
'        current_line_height = self.text_edit.document().documentMargin()',
'        if current_line_height <= 0:',
'            current_line_height = 1.2',
'        line_height_spin.setValue(current_line_height / current_font.pointSize())',
'        line_height_spin.setRange(0.8, 3.0)',
'        line_height_spin.setSingleStep(0.1)',
'        line_height_layout.addWidget(line_height_spin)',
'        layout.addLayout(line_height_layout)',
'',
'        # 字重（粗细）选择',
'        weight_layout = QHBoxLayout()',
'        weight_layout.addWidget(QLabel("粗细:"))',
'        weight_combo = QComboBox()',
'        from PyQt5.QtGui import QFont',
'        weight_combo.addItem("正常", QFont.Normal)',
'        weight_combo.addItem("粗体", QFont.Bold)',
'        # 匹配当前字重',
'        current_weight = current_font.weight()',
'        if current_weight >= QFont.Bold:',
'            weight_combo.setCurrentIndex(1)',
'        else:',
'            weight_combo.setCurrentIndex(0)',
'        weight_layout.addWidget(weight_combo)',
'        layout.addLayout(weight_layout)',
'',
'        # 按钮',
'        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)',
'        buttons.accepted.connect(accept)',
'        buttons.rejected.connect(dialog.reject)',
'        layout.addWidget(buttons)',
'',
'        # 应用设置',
'        def accept():',
'            from PyQt5.QtGui import QFont',
'            new_font = font_combo.currentFont()',
'            new_font.setPointSize(size_spin.value())',
'            new_font.setWeight(weight_combo.currentData())',
'            self.text_edit.setFont(new_font)',
'            # 设置行高',
'            self.text_edit.document().setDocumentMargin(line_height_spin.value() * new_font.pointSize())',
'            # 保存设置',
'            self.settings.setValue("font_family", new_font.family())',
'            self.settings.setValue("font_size", size_spin.value())',
'            self.settings.setValue("font_weight", new_font.weight())',
'            self.settings.setValue("line_spacing", line_height_spin.value())',
'            self.status_bar.showMessage(f"字体设置已更新：{new_font.family()} {new_font.pointSize()}pt", 3000)',
'            dialog.accept()',
'',
'        dialog.exec_()',
''
]
# 替换原有方法
new_lines = lines[:start_line] + [line + '\n' for line in new_method] + lines[end_line:]
content = ''.join(new_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ 完整重写 open_font_settings 方法，共 {len(new_method)} 行")
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")