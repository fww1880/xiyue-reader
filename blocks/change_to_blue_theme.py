import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 替换工具栏样式为蓝色调，无黑边
old_toolbar_css = """            QToolBar {
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
            }"""
new_toolbar_css = """            QToolBar {
                spacing: 3px;
                padding: 5px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border: none;
            }
            QToolButton {
                border: none;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #E3F2FD);
                padding: 4px 8px;
                margin: 2px;
                min-width: 60px;
                color: #1565C0;
                font-weight: bold;
            }
            QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BBDEFB, stop:1 #90CAF9);
            }
            QToolButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90CAF9, stop:1 #64B5F6);
                padding: 5px 7px 3px 9px;
            }"""
if old_toolbar_css in content:
    content = content.replace(old_toolbar_css, new_toolbar_css)
    print("✅ 修改1：工具栏已更新为蓝色调，移除黑边")
else:
    print("⚠️ 修改1：未找到原工具栏样式")
# 2. 替换书架 (QDockWidget) 样式为蓝色调，无黑边
old_dock_css_start = "        # 设置书架立体样式"
if old_dock_css_start in content:
    # 找到整个 setStyleSheet 块并替换
    import re
    # 匹配从 setStyleSheet(""" 到 """) 的内容
    pattern = re.compile(r'self\.bookshelf_dock\.setStyleSheet\(""".*?"""\)', re.DOTALL)
    new_dock_style = '''self.bookshelf_dock.setStyleSheet("""
            QDockWidget {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F0F4F8, stop:1 #E1EBF5);
            }
            QDockWidget::title {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90CAF9, stop:1 #64B5F6);
                padding: 6px;
                color: white;
                font-weight: bold;
                border: none;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                border: none;
                background: #E3F2FD;
                border-radius: 3px;
            }
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                background: #BBDEFB;
            }
        """)'''
    content = pattern.sub(new_dock_style, content)
    print("✅ 修改2：书架已更新为蓝色调，移除黑边")
else:
    print("⚠️ 修改2：未找到书架样式代码")
# 3. 替换正文区域 (QTextEdit) 样式为白色/浅蓝，无黑边
old_text_css = """        # 设置正文区域立体样式
        self.text_edit.setStyleSheet(\"\"\"
            QTextEdit {
                border: 2px solid #999;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f8f8);
                padding: 10px;
            }
        \"\"\")"""
new_text_css = """        # 设置正文区域样式（清爽无框）
        self.text_edit.setStyleSheet(\"\"\"
            QTextEdit {
                border: none;
                background-color: #FAFAFA;
                padding: 15px;
                font-size: 18px;
            }
        \"\"\")"""
if old_text_css in content:
    content = content.replace(old_text_css, new_text_css)
    print("✅ 修改3：正文区域已更新为浅灰/白底，移除黑框")
else:
    print("⚠️ 修改3：未找到正文区域样式")
# 4. 移除或修改窗口阴影，避免看起来像黑边
# 找到 setGraphicsEffect 部分并调整颜色为淡蓝或移除
old_shadow = """        shadow.setColor(QColor(0, 0, 0, 80))"""
new_shadow = """        shadow.setColor(QColor(33, 150, 243, 40))  # 淡蓝色阴影"""
if old_shadow in content:
    content = content.replace(old_shadow, new_shadow)
    print("✅ 修改4：窗口阴影改为淡蓝色，视觉更柔和")
else:
    print("⚠️ 修改4：未找到阴影设置")
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