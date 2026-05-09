import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复 toggle_focus_mode
old_focus = '''    def toggle_focus_mode(self):
        """切换专注模式"""
        if self.bookshelf_panel.isVisible():
            self.bookshelf_panel.hide()
        else:
            self.bookshelf_panel.show()'''
new_focus = '''    def toggle_focus_mode(self):
        """切换专注模式（隐藏/显示书架浮动窗口）"""
        if self.bookshelf_dock.isVisible():
            self.bookshelf_dock.hide()
        else:
            self.bookshelf_dock.show()'''
content = content.replace(old_focus, new_focus)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 专注模式已修复！")
print("修改内容：")
print("- 将 bookshelf_panel 改为 bookshelf_dock")
print("- 现在专注模式会正确隐藏/显示浮动书架窗口")