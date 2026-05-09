import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 在 __init__ 中初始化书签列表 =====
old_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.chapter_positions = []'''
new_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.chapter_positions = []
        self.bookmarks = []  # 当前书籍的书签列表'''
content = content.replace(old_init_vars, new_init_vars)
# ===== 2. 在工具栏添加书签按钮 =====
# 找到 create_tool_bar 方法，在专注模式后添加书签按钮
toolbar_marker = "focus_action = QAction(\"🧘 专注\", self)"
if toolbar_marker in content:
    bookmark_btn_code = '''
        
        toolbar.addSeparator()
        
        # 书签功能
        add_bm_action = QAction("🔖 加签", self)
        add_bm_action.setShortcut("Ctrl+D")
        add_bm_action.triggered.connect(self.add_bookmark)
        toolbar.addAction(add_bm_action)
        
        list_bm_action = QAction("📋 书签", self)
        list_bm_action.triggered.connect(self.show_bookmark_list)
        toolbar.addAction(list_bm_action)'''
    content = content.replace(toolbar_marker, toolbar_marker + bookmark_btn_code)
    print("✅ 工具栏已添加书签按钮")
# ===== 3. 添加书签相关方法 =====
bookmark_methods = '''
    def add_bookmark(self):
        """添加书签"""
        if not self.current_book_path:
            self.status_bar.showMessage("⚠️ 请先打开一本书籍", 3000)
            return
        
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        block = cursor.blockNumber()
        text_block = cursor.block().text()[:50] # 取前50字作为预览
        
        # 检查是否重复
        for bm in self.bookmarks:
            if bm['pos'] == pos:
                self.status_bar.showMessage("⚠️ 该位置已有书签", 3000)
                return
        
        bookmark = {
            'pos': pos,
            'title': f"书签 {len(self.bookmarks)+1}",
            'preview': text_block,
            'time': self.get_current_time()
        }
        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        self.status_bar.showMessage(f"✅ 书签已添加：{text_block}...", 3000)
    
    def show_bookmark_list(self):
        """显示书签管理对话框"""
        if not self.current_book_path:
            self.status_bar.showMessage("⚠️ 请先打开一本书籍", 3000)
            return
        
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📑 书签管理")
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 书签列表
        self.bm_list_widget = QListWidget()
        self.refresh_bookmark_list()
        layout.addWidget(self.bm_list_widget)
        
        # 按钮组
        btn_layout = QHBoxLayout()
        
        jump_btn = QPushButton("跳转到")
        jump_btn.clicked.connect(lambda: self.jump_to_selected_bookmark())
        btn_layout.addWidget(jump_btn)
        
        del_btn = QPushButton("删除")
        del_btn.clicked.connect(lambda: self.delete_selected_bookmark())
        btn_layout.addWidget(del_btn)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        # 双击跳转
        self.bm_list_widget.itemDoubleClicked.connect(lambda item: self.jump_to_selected_bookmark(dialog))
        
        dialog.exec_()
    
    def refresh_bookmark_list(self):
        """刷新书签列表显示"""
        self.bm_list_widget.clear()
        for i, bm in enumerate(self.bookmarks):
            display_text = f"{i+1}. {bm['title']} - {bm['preview']}... ({bm['time']})"
            item = self.bm_list_widget.addItem(display_text)
    
    def jump_to_selected_bookmark(self, dialog=None):
        """跳转到选中的书签"""
        current_row = self.bm_list_widget.currentRow()
        if current_row == -1:
            self.status_bar.showMessage("⚠️ 请先选择一个书签", 3000)
            return
        
        bm = self.bookmarks[current_row]
        cursor = self.text_edit.textCursor()
        cursor.setPosition(bm['pos'])
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()
        self.status_bar.showMessage(f"📍 已跳转到：{bm['title']}", 3000)
        
        if dialog:
            dialog.close()
    
    def delete_selected_bookmark(self):
        """删除选中的书签"""
        current_row = self.bm_list_widget.currentRow()
        if current_row == -1:
            self.status_bar.showMessage("⚠️ 请先选择一个书签", 3000)
            return
        
        bm = self.bookmarks.pop(current_row)
        self.save_bookmarks()
        self.refresh_bookmark_list()
        self.status_bar.showMessage(f"🗑️ 已删除书签：{bm['title']}", 3000)
    
    def save_bookmarks(self):
        """保存书签到本地"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.settings.setValue(key, self.bookmarks)
    
    def load_bookmarks(self):
        """加载书签"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.bookmarks = self.settings.value(key, [])
            if not isinstance(self.bookmarks, list):
                self.bookmarks = []
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M")
'''
# 在文件末尾添加这些方法 (在 main 函数之前)
main_func_pos = content.find('\ndef main():')
if main_func_pos != -1:
    content = content[:main_func_pos] + bookmark_methods + content[main_func_pos:]
    print("✅ 书签功能方法已添加")
else:
    print("⚠️ 未找到 main 函数位置")
# ===== 4. 修改 load_book 方法，加载时读取书签 =====
load_book_marker = "self.current_book_path = file_path"
if load_book_marker in content:
    load_bookmarks_code = "\n            self.load_bookmarks() # 加载书签"
    content = content.replace(load_book_marker, load_book_marker + load_bookmarks_code)
    print("✅ load_book 已更新，自动加载书签")
# 保存文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("🚀 书签功能开发完成！")