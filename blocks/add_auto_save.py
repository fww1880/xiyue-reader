import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 在 __init__ 中添加 closeEvent 绑定
old_init_end = '''        # 启用键盘快捷键
        self.text_edit.keyPressEvent = self.keyboard_pagination'''
new_init_end = '''        # 启用键盘快捷键
        self.text_edit.keyPressEvent = self.keyboard_pagination
        
        # 注册关闭事件处理
        self.closeEvent = self.on_close'''
content = content.replace(old_init_end, new_init_end)
print("✅ 已注册关闭事件处理")
# 2. 添加 on_close 方法（在 save_bookmarks 方法附近）
close_method = '''
    def on_close(self, event):
        """关闭窗口时自动保存所有状态"""
        print("💾 正在保存阅读状态...")
        # 保存当前打开的书籍路径
        if self.current_book_path:
            self.settings.setValue("last_opened_book", self.current_book_path)
        # 保存当前阅读进度
        cursor = self.text_edit.textCursor()
        if self.current_book_path:
            self.settings.setValue(f"position_{hash(self.current_book_path)}", cursor.position())
        # 保存字体设置
        font = self.text_edit.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())
        self.settings.setValue("font_weight", font.weight())
        line_height = self.text_edit.document().documentMargin() / font.pointSize() if font.pointSize() > 0 else 1.2
        self.settings.setValue("line_spacing", line_height)
        # 保存当前主题模式
        self.settings.setValue("current_theme", self.current_theme)
        # 保存窗口大小和位置
        self.settings.setValue("window_geometry", self.saveGeometry())
        self.settings.setValue("window_state", self.saveState())
        # 保存书架面板状态（是否浮动、位置等）
        self.settings.setValue("bookshelf_floating", self.bookshelf_dock.isFloating())
        self.settings.setValue("bookshelf_visible", self.bookshelf_dock.isVisible())
        # 保存所有书签（已经在添加/删除时实时保存，这里再确保一次）
        self.save_bookmarks()
        print("✅ 所有状态已保存！")
        event.accept()
    
    def restore_state(self):
        """启动时恢复上次关闭时的状态"""
        # 恢复窗口大小和位置
        geometry = self.settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.settings.value("window_state")
        if state:
            self.restoreState(state)
        # 恢复书架面板状态
        floating = self.settings.value("bookshelf_floating", False)
        visible = self.settings.value("bookshelf_visible", True)
        if isinstance(floating, str):
            floating = floating == "true"
        if isinstance(visible, str):
            visible = visible == "true"
        self.bookshelf_dock.setFloating(floating)
        self.bookshelf_dock.setVisible(visible)
        # 恢复字体设置
        font_family = self.settings.value("font_family", "Microsoft YaHei")
        font_size = int(self.settings.value("font_size", 18))
        font_weight = int(self.settings.value("font_weight", 50))  # QFont.Normal
        line_spacing = float(self.settings.value("line_spacing", 1.2))
        from PyQt5.QtGui import QFont
        font = QFont(font_family, font_size)
        font.setWeight(font_weight)
        self.text_edit.setFont(font)
        self.text_edit.document().setDocumentMargin(line_spacing * font_size)
        # 恢复主题模式
        theme = self.settings.value("current_theme", "day")
        self.current_theme = theme
        # 恢复最后打开的书籍和阅读进度
        last_book = self.settings.value("last_opened_book")
        if last_book and os.path.exists(last_book):
            self.open_book(last_book)
            # 恢复阅读进度
            pos_key = f"position_{hash(last_book)}"
            last_pos = self.settings.value(pos_key, 0)
            if last_pos:
                cursor = self.text_edit.textCursor()
                cursor.setPosition(int(last_pos))
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                self.status_bar.showMessage(f"📖 已恢复到上次阅读进度", 3000)
'''
# 找到 save_bookmarks 方法的位置，在它前面插入 close_event 相关代码
if 'def save_bookmarks(self):' in content:
    idx = content.find('def save_bookmarks(self):')
    # 找到这个方法的开头（往前找空行）
    insert_idx = content.rfind('\n', 0, idx)
    insert_idx = content.rfind('\n', 0, insert_idx)
    content = content[:insert_idx] + '\n' + close_method + '\n' + content[insert_idx:]
    print("✅ 已添加 on_close 和 restore_state 方法")
else:
    print("⚠️ 未找到 save_bookmarks 方法，尝试其他方式...")
# 3. 在 init_ui 或 load_settings 后调用 restore_state
if 'self.load_settings()' in content:
    old_load = 'self.load_settings()'
    new_load = '''self.load_settings()
        self.restore_state()'''
    content = content.replace(old_load, new_load)
    print("✅ 已在启动时调用 restore_state 恢复状态")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")