import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 修改 add_bookmark 方法：支持多条 + 添加日期 =====
old_add_bm = '''    def add_bookmark(self):
        """添加书签"""
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        
        # 检查是否已存在
        if pos in self.bookmarks:
            QMessageBox.information(self, "提示", "当前位置已有书签！")
            return
        
        self.bookmarks[pos] = {
            'position': pos,
            'preview': self.get_position_preview(pos)
        }
        self.save_bookmarks()
        QMessageBox.information(self, "成功", "书签已添加！")'''
new_add_bm = '''    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        from datetime import datetime
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        
        # 不再检查重复，允许同一位置多条书签
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 使用列表存储同一位置的多个书签
        if not hasattr(self, 'bookmark_list'):
            self.bookmark_list = []
        
        self.bookmark_list.append({
            'position': pos,
            'preview': self.get_position_preview(pos),
            'time': timestamp
        })
        self.save_bookmarks()
        QMessageBox.information(self, "成功", f"书签已添加！\\n时间：{timestamp}")'''
content = content.replace(old_add_bm, new_add_bm)
# ===== 2. 修改 refresh_bookmark_list 方法：显示日期 =====
old_refresh = '''    def refresh_bookmark_list(self):
        """刷新书签列表"""
        self.bm_list_widget.clear()
        for pos, bm in sorted(self.bookmarks.items(), key=lambda x: x[0]):
            item_text = f"{bm['preview'][:30]}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, pos)
            self.bm_list_widget.addItem(item)'''
new_refresh = '''    def refresh_bookmark_list(self):
        """刷新书签列表（显示日期）"""
        self.bm_list_widget.clear()
        if not hasattr(self, 'bookmark_list') or not self.bookmark_list:
            return
        # 按位置排序
        for i, bm in enumerate(sorted(self.bookmark_list, key=lambda x: x['position'])):
            item_text = f"[{bm['time']}] {bm['preview'][:30]}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, bm['position'])
            item.setData(Qt.UserRole + 1, i)  # 存储索引
            self.bm_list_widget.addItem(item)'''
content = content.replace(old_refresh, new_refresh)
# ===== 3. 修改 save_bookmarks 和 load_bookmarks 支持新结构 =====
old_save = '''    def save_bookmarks(self):
        """保存书签到文件"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)'''
new_save = '''    def save_bookmarks(self):
        """保存书签列表到文件"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        data = getattr(self, 'bookmark_list', [])
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)'''
content = content.replace(old_save, new_save)
old_load = '''    def load_bookmarks(self):
        """从文件加载书签"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        if os.path.exists(bookmark_file):
            with open(bookmark_file, 'r', encoding='utf-8') as f:
                self.bookmarks = json.load(f)'''
new_load = '''    def load_bookmarks(self):
        """从文件加载书签列表"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        if os.path.exists(bookmark_file):
            with open(bookmark_file, 'r', encoding='utf-8') as f:
                self.bookmark_list = json.load(f)'''
content = content.replace(old_load, new_load)
# ===== 4. 修改 jump_to_selected_bookmark 使用新数据结构 =====
old_jump = '''    def jump_to_selected_bookmark(self):
        """跳转到选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "提示", "请先选择一个书签！")
            return
        pos = item.data(Qt.UserRole)
        self.text_edit.moveCursor(QTextCursor.Start)
        for _ in range(pos):
            self.text_edit.moveCursor(QTextCursor.NextCharacter)
        self.text_edit.ensureCursorVisible()'''
new_jump = '''    def jump_to_selected_bookmark(self, checked=None):
        """跳转到选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            return
        pos = item.data(Qt.UserRole)
        self.text_edit.moveCursor(QTextCursor.Start)
        for _ in range(pos):
            self.text_edit.moveCursor(QTextCursor.NextCharacter)
        self.text_edit.ensureCursorVisible()'''
content = content.replace(old_jump, new_jump)
# ===== 5. 初始化时初始化列表 =====
old_init_bm = '''        # 书签功能
        self.bookmarks = {}'''
new_init_bm = '''        # 书签功能
        self.bookmark_list = []'''
content = content.replace(old_init_bm, new_init_bm)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 书签功能已升级：支持无限添加 + 显示日期时间！")