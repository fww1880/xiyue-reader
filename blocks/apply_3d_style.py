import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 替换 QToolBar 的样式为立体风格
old_toolbar_css = '''            QToolBar {
                spacing: 2px;
            }
            QToolButton {
                border: 1px solid #777;
                border-radius: 4px;
                background-color: #f0f0f0;
                padding: 2px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-color: #555;
            }
            QToolButton:pressed {
                background-color: #ccc;
                border: 1px inset #777;
                padding: 3px 1px 1px 3px;
            }'''
new_toolbar_css = '''            QToolBar {
                spacing: 3px;
                padding: 5px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8e8e8, stop:1 #d0d0d0);
                border-bottom: 2px solid #a0a0a0;
            }
            QToolButton {
                border: 1px solid #999;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #e0e0e0);
                padding: 4px 8px;
                margin: 2px;
                min-width: 60px;
            }
            QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:1 #d8e8f8);
                border-color: #666;
            }
            QToolButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0c0c0, stop:1 #d0d0d0);
                border: 1px inset #999;
                padding: 5px 7px 3px 9px;
            }'''
if old_toolbar_css in content:
    content = content.replace(old_toolbar_css, new_toolbar_css)
    print("✅ 修改1：工具栏已升级为立体渐变风格")
else:
    print("⚠️ 修改1：未找到原工具栏样式")
# 2. 查找并替换 QDockWidget (书架) 的样式
# 先看看有没有 QDockWidget 相关样式
if 'QDockWidget' not in content:
    # 在 init_ui 方法中，创建 bookshelf_dock 后添加样式
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'self.bookshelf_dock = QDockWidget' in line:
            # 在这几行后面添加样式设置
            insert_pos = i + 5
            style_code = [
                '        # 设置书架立体样式',
                '        self.bookshelf_dock.setStyleSheet("""',
                '            QDockWidget {',
                '                border: 2px solid #888;',
                '                border-radius: 8px;',
                '                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,',
                '                    stop:0 #f5f5f5, stop:1 #e8e8e8);',
                '                titlebar-close-icon: none;',
                '                titlebar-normal-icon: none;',
                '            }',
                '            QDockWidget::title {',
                '                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,',
                '                    stop:0 #d0d0d0, stop:1 #b0b0b0);',
                '                padding: 4px;',
                '                border-top-left-radius: 6px;',
                '                border-top-right-radius: 6px;',
                '                font-weight: bold;',
                '            }',
                '            QDockWidget::close-button, QDockWidget::float-button {',
                '                border: 1px solid #777;',
                '                border-radius: 3px;',
                '                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,',
                '                    stop:0 #e8e8e8, stop:1 #c8c8c8);',
                '            }',
                '        """)',
            ]
            for j, code_line in enumerate(style_code):
                lines.insert(insert_pos + j, code_line)
            print(f"✅ 修改2：已在 L{insert_pos+1} 添加书架立体样式")
            break
    content = '\n'.join(lines)
else:
    print("✅ 修改2：QDockWidget 样式已存在")
# 3. 给 QTextEdit (正文区域) 添加立体边框
# 查找 text_edit 的创建或样式设置
lines = content.split('\n')
found_text_edit = False
for i, line in enumerate(lines):
    if 'self.text_edit = QTextEdit' in line or 'self.text_edit.setStyleSheet' in line:
        found_text_edit = True
        # 检查后面几行是否有 setStyleSheet
        has_style = False
        for j in range(i, min(len(lines), i+10)):
            if 'setStyleSheet' in lines[j]:
                has_style = True
                break
        if not has_style:
            # 在创建后添加样式
            insert_pos = i + 1
            style_lines = [
                '        # 设置正文区域立体样式',
                '        self.text_edit.setStyleSheet("""',
                '            QTextEdit {',
                '                border: 2px solid #999;',
                '                border-radius: 8px;',
                '                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,',
                '                    stop:0 #ffffff, stop:1 #f8f8f8);',
                '                padding: 10px;',
                '            }',
                '        """)',
            ]
            for k, sl in enumerate(style_lines):
                lines.insert(insert_pos + k, sl)
            print(f"✅ 修改3：已在 L{insert_pos+1} 添加正文区域立体样式")
            break
content = '\n'.join(lines)
# 4. 给主窗口添加阴影效果（如果可能）
# 查找 QMainWindow 的初始化
if 'setGraphicsEffect' not in content:
    # 在 init_ui 末尾添加阴影
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def init_ui(self):' in line:
            # 找到 init_ui 的结束位置
            for j in range(i+1, len(lines)):
                if lines[j].strip().startswith('def ') and '    def ' in lines[j]:
                    # 在这个 def 之前插入阴影代码
                    insert_pos = j
                    shadow_code = [
                        '',
                        '        # 设置主窗口阴影效果',
                        '        from PyQt5.QtWidgets import QGraphicsDropShadowEffect',
                        '        from PyQt5.QtGui import QColor',
                        '        shadow = QGraphicsDropShadowEffect()',
                        '        shadow.setBlurRadius(20)',
                        '        shadow.setXOffset(3)',
                        '        shadow.setYOffset(3)',
                        '        shadow.setColor(QColor(0, 0, 0, 80))',
                        '        self.setGraphicsEffect(shadow)',
                    ]
                    for k, sc in enumerate(shadow_code):
                        lines.insert(insert_pos + k, sc)
                    print(f"✅ 修改4：已在 L{insert_pos+1} 添加窗口阴影效果")
                    break
            break
    content = '\n'.join(lines)
else:
    print("✅ 修改4：窗口阴影效果已存在")
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