import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 show_about_dialog 方法
old_about = '''    def show_about_dialog(self):
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
        )'''
new_about = '''    def show_about_dialog(self):
        """显示关于对话框"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于 喜阅",
            "<h2>📖 木木和叶子的喜阅</h2>"
            "<p>版本：2026.5</p>"
            "<hr>"
            "<p>一款本地小说阅读器，让阅读更愉悦。</p>"
            "<p>支持多种格式、书签管理、自动滚屏、翻页动画。</p>"
            "<hr>"
            "<p style='color: #888;'>© 2026 木木和叶子</p>"
        )'''
if old_about in content:
    content = content.replace(old_about, new_about)
    print("✅ 已修改关于对话框内容")
else:
    print("⚠️ 未找到完全匹配的旧代码，尝试模糊匹配...")
    if '木木的喜阅' in content:
        content = content.replace('木木的喜阅', '木木和叶子的喜阅')
        content = content.replace('© 2026 木木', '© 2026 木木和叶子')
        print("✅ 已替换相关文本")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")