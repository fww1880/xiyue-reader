import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复逻辑：将 def accept() 移到 buttons.accepted.connect(accept) 之前
# 查找出问题的代码段
old_code = """        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        # 应用设置
        def accept():"""
new_code = """        # 应用设置
        def accept():
            from PyQt5.QtGui import QFont
            new_font = font_combo.currentFont()
            new_font.setPointSize(size_spin.value())
            new_font.setWeight(weight_combo.currentData())
            self.text_edit.setFont(new_font)
            # 设置行高
            self.text_edit.document().setDocumentMargin(line_height_spin.value() * new_font.pointSize())
            # 保存设置
            self.settings.setValue("font_family", new_font.family())
            self.settings.setValue("font_size", size_spin.value())
            self.settings.setValue("font_weight", new_font.weight())
            self.settings.setValue("line_spacing", line_height_spin.value())
            self.status_bar.showMessage(f"字体设置已更新：{new_font.family()} {new_font.pointSize()}pt", 3000)
            dialog.accept()
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        # 占位（原 accept 定义已移走，此处删除）
        def accept_placeholder():"""
# 替换
if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ 修复1：已调整 accept 函数定义顺序，解决闪退")
else:
    print("⚠️ 未找到精确匹配，尝试更通用的修复...")
    # 如果缩进不同，我们直接重写整个方法会更稳妥，或者手动调整
    # 这里先尝试查找并删除后面多余的 accept 定义，并在前面添加
    
    # 查找 accept 定义的位置
    lines = content.split('\n')
    new_lines = []
    accept_code = []
    in_accept = False
    accept_found = False
    
    # 先提取 accept 函数的内容
    for line in lines:
        if '        def accept():' in line:
            in_accept = True
            accept_found = True
            continue
        if in_accept:
            if line.startswith('            ') or line.strip() == '':
                accept_code.append(line)
            else:
                in_accept = False
                # 如果不是空行且不缩进，说明 accept 结束了，这行要加回去
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    if accept_found:
        print("✅ 提取到 accept 函数内容")
        # 重新组合：在 buttons 之前插入 accept
        final_lines = []
        inserted = False
        for line in new_lines:
            if '        buttons.accepted.connect(accept)' in line and not inserted:
                # 在这之前插入 accept 定义
                final_lines.append('        # 应用设置')
                final_lines.append('        def accept():')
                final_lines.extend(accept_code)
                inserted = True
            final_lines.append(line)
        
        content = '\n'.join(final_lines)
        print("✅ 修复1：已重构代码顺序")
    else:
        print("❌ 未能自动修复，请检查代码")
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