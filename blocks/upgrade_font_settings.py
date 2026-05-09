import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 修改1: 修改默认字号从16 → 18 =====
old_default = "        self.font_size = self.settings.value('font_size', 16, int)"
new_default = "        self.font_size = self.settings.value('font_size', 18, int)"
if old_default in content:
    content = content.replace(old_default, new_default)
    print("✅ 修改1：默认字号已改为 18")
else:
    print("⚠️ 修改1：未找到默认字号行")
# ===== 修改2: 升级 open_font_settings 方法，增加字体选择和粗细选择 =====
# 找到 open_font_settings 方法开始，替换整个方法
old_start = "    def open_font_settings(self):\n        \"\"\"打开字体设置对话框\"\"\"\n        dialog = QDialog(self)\n        dialog.setWindowTitle(\"字体设置\")\n        layout = QVBoxLayout(dialog)\n\n        # 字号设置"
new_start = "    def open_font_settings(self):\n        \"\"\"打开字体设置对话框\"\"\"\n        from PyQt5.QtWidgets import QFontComboBox, QComboBox\n        dialog = QDialog(self)\n        dialog.setWindowTitle(\"字体设置\")\n        dialog.resize(400, 300)\n        layout = QVBoxLayout(dialog)\n\n        # 字体选择\n        font_layout = QHBoxLayout()\n        font_layout.addWidget(QLabel(\"字体:\"))\n        font_combo = QFontComboBox()\n        current_font = self.text_edit.font()\n        font_combo.setCurrentFont(current_font)\n        font_layout.addWidget(font_combo)\n        layout.addLayout(font_layout)\n\n        # 字号设置"
if old_start in content:
    content = content.replace(old_start, new_start)
    print("✅ 修改2：已添加字体选择框")
else:
    print("⚠️ 修改2：未匹配到起始代码")
# 找到行高设置之后，按钮之前，添加粗细选择
old_middle = """        # 行高设置
        line_height_layout = QHBoxLayout()
        line_height_layout.addWidget(QLabel(\"行高:\"))
        line_height_spin = QDoubleSpinBox()
        current_line_height = self.text_edit.document().documentMargin()
        if current_line_height <= 0:
            current_line_height = 1.2
        line_height_spin.setValue(current_line_height)
        line_height_spin.setRange(0.8, 3.0)
        line_height_spin.setSingleStep(0.1)
        line_height_layout.addWidget(line_height_spin)
        layout.addLayout(line_height_layout)
        # 按钮"""
new_middle = """        # 行高设置
        line_height_layout = QHBoxLayout()
        line_height_layout.addWidget(QLabel(\"行高:\"))
        line_height_spin = QDoubleSpinBox()
        current_line_height = self.text_edit.document().documentMargin()
        if current_line_height <= 0:
            current_line_height = 1.2
        line_height_spin.setValue(current_line_height)
        line_height_spin.setRange(0.8, 3.0)
        line_height_spin.setSingleStep(0.1)
        line_height_layout.addWidget(line_height_spin)
        layout.addLayout(line_height_layout)
        # 字重（粗细）选择
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel(\"粗细:\"))
        weight_combo = QComboBox()
        from PyQt5.QtGui import QFont
        weight_combo.addItem(\"正常\", QFont.Normal)
        weight_combo.addItem(\"粗体\", QFont.Bold)
        # 匹配当前字重
        current_weight = current_font.weight()
        if current_weight >= QFont.Bold:
            weight_combo.setCurrentIndex(1)
        else:
            weight_combo.setCurrentIndex(0)
        weight_layout.addWidget(weight_combo)
        layout.addLayout(weight_layout)
        # 按钮"""
if old_middle in content:
    content = content.replace(old_middle, new_middle)
    print("✅ 修改3：已添加粗细选择")
else:
    print("⚠️ 修改3：未匹配到中间代码")
# 修改确认后的代码，应用字体、字号、粗细
old_apply = """        # 应用设置
        def accept():
            font = current_font
            font.setPointSize(size_spin.value())
            self.text_edit.setFont(font)
            # 设置行高
            self.text_edit.document().setDocumentMargin(line_height_spin.value() * font.pointSize())
            self.settings.setValue('font_size', size_spin.value())
            self.settings.setValue('line_spacing', line_height_spin.value())
            self.status_bar.showMessage(f\"字体设置已更新：字号 {size_spin.value()}\", 3000)
            dialog.accept()"""
new_apply = """        # 应用设置
        def accept():
            from PyQt5.QtGui import QFont
            new_font = font_combo.currentFont()
            new_font.setPointSize(size_spin.value())
            new_font.setWeight(weight_combo.currentData())
            self.text_edit.setFont(new_font)
            # 设置行高
            self.text_edit.document().setDocumentMargin(line_height_spin.value() * new_font.pointSize())
            # 保存设置
            self.settings.setValue('font_family', new_font.family())
            self.settings.setValue('font_size', size_spin.value())
            self.settings.setValue('font_weight', new_font.weight())
            self.settings.setValue('line_spacing', line_height_spin.value())
            self.status_bar.showMessage(f\"字体设置已更新：{new_font.family()} {new_font.pointSize()}pt\", 3000)
            dialog.accept()"""
if old_apply in content:
    content = content.replace(old_apply, new_apply)
    print("✅ 修改4：已更新应用设置逻辑，保存字体家族和粗细")
else:
    print("⚠️ 修改4：未匹配到应用代码")
# 修改初始化，加载保存的字体设置
# 找到 init_ui 后的加载部分
old_load_start = "    def load_settings(self):\n        \"\"\"加载设置\"\"\"\n        self.settings = QSettings('NovelReader', 'Settings')\n        self.font_size = self.settings.value('font_size', 18, int)\n        self.line_spacing = self.settings.value('line_spacing', 1.5, float)\n        self.theme = self.settings.value('theme', 'light', str)"
new_load_start = "    def load_settings(self):\n        \"\"\"加载设置\"\"\"\n        self.settings = QSettings('NovelReader', 'Settings')\n        self.font_size = self.settings.value('font_size', 18, int)\n        self.line_spacing = self.settings.value('line_spacing', 1.5, float)\n        self.font_family = self.settings.value('font_family', None, str)\n        self.font_weight = self.settings.value('font_weight', None, int)\n        self.theme = self.settings.value('theme', 'light', str)"
if old_load_start in content:
    content = content.replace(old_load_start, new_load_start)
    print("✅ 修改5：已在 load_settings 添加字体家族和粗细加载")
else:
    print("⚠️ 修改5：未匹配到 load_settings 起始")
# 在 apply_theme 或 init_ui 中应用字体设置
# 查找 where 应用字体初始化
lines = content.split('\n')
found = False
for i, line in enumerate(lines):
    if 'self.text_edit.setFont' in line:
        # 在这行之后添加加载保存的字体设置
        if i+2 < len(lines) and not 'self.font_size' in lines[i+1]:
            lines.insert(i+1, '        # 加载保存的字体设置')
            lines.insert(i+2, '        if hasattr(self, \"font_family\") and self.font_family:')
            lines.insert(i+3, '            current_font = self.text_edit.font()')
            lines.insert(i+4, '            current_font.setFamily(self.font_family)')
            lines.insert(i+5, '            if hasattr(self, \"font_weight\") and self.font_weight:')
            lines.insert(i+6, '                current_font.setWeight(self.font_weight)')
            lines.insert(i+7, '            self.text_edit.setFont(current_font)')
            content = '\n'.join(lines)
            print("✅ 修改6：已添加字体设置应用代码")
            found = True
            break
if not found:
    print("⚠️ 修改6：未找到插入位置，可能需要手动检查")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")