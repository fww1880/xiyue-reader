import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 替换 L1180-L1193 (索引 1179-1192)
# 替换为正确的内容
new_block = [
    '    def show_bookmark_list(self):\n',
    '        """显示书签列表（显示书架面板并刷新）"""\n',
    '        self.bookshelf_dock.show()\n',
    '        self.refresh_bookmark_list()\n',
    '\n',
    '    def show_about_dialog(self):\n',
    '        """显示关于对话框"""\n',
    '        from PyQt5.QtWidgets import QMessageBox\n',
    '        QMessageBox.about(self, "关于 喜阅",\n',
    '            "<h2>📖 木木的喜阅</h2>"\n',
    '            "<p>版本：2026.5</p>"\n',
    '            "<hr>"\n',
    '            "<p>一款本地小说阅读器，让阅读更愉悦。</p>"\n',
    '            "<p>支持多种格式、书签管理、自动滚屏、翻页动画。</p>"\n',
    '            "<hr>"\n',
    '            "<p style=\'color: #888;\'>© 2026 木木</p>"\n',
    '        )\n',
    '\n',
]
# 替换 L1180-L1193 (索引 1179-1192)
lines[1179:1193] = new_block
content = ''.join(lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 已直接替换 L1180-L1193 为正确内容")
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")