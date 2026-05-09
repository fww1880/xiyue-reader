import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 给 about_action 添加 triggered 绑定
old_about = """        about_action = QAction(\"关于\", self)
        help_menu.addAction(about_action)"""
new_about = """        about_action = QAction(\"关于\", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)"""
if old_about in content:
    content = content.replace(old_about, new_about)
    print("✅ 修改1：已绑定 about_action 到 show_about_dialog")
else:
    print("⚠️ 修改1：未找到精确匹配")
# 2. 添加 show_about_dialog 方法
# 找到 help_menu 相关代码附近，在最后一个方法后面添加
# 更好的方式：在类的最后一个方法后添加
lines = content.split('\n')
# 找到类的结束位置（最后一个 def 之后）
last_def = 0
for i, line in enumerate(lines):
    if line.strip().startswith('def ') and '    def ' in line:
        last_def = i
# 在最后一个方法后插入
about_method = '''
    def show_about_dialog(self):
        """显示关于对话框"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于 喜阅",
            "<h2>📖 木木的喜阅</h2>"
            "<p>版本：2026.5</p>"
            "<hr>"
            "<p>一款本地小说阅读器，让阅读更愉悦。</p>"
            "<p>支持多种格式、书签管理、自动滚屏、翻页动画。</p>"
            "<hr>"
            "<p style='color: #888;'>© 2026 木木</p>"
        )
'''
# 在最后一个 def 之后插入
insert_line = last_def + 1
while insert_line < len(lines) and lines[insert_line].strip() == '':
    insert_line += 1
lines.insert(insert_line, about_method)
content = '\n'.join(lines)
print(f"✅ 修改2：已在 L{insert_line+1} 添加 show_about_dialog 方法")
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