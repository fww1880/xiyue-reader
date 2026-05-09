import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 重写 add_bookmark 方法 =====
old_add = '''    def add_bookmark(self):
        """添加书签"""
        if not self.current_book_path:
            QMessageBox.warning(self, "警告", "请先打开一本书籍")
            return
            
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        block = cursor.blockNumber()
        text_block = cursor.block().text()
        preview = text_block[:50] if len(text_block) > 50 else text_block
        
        bookmarks = self.settings.value(f"bookmarks_{self.current_book_path}", [])
        if not isinstance(bookmarks, list):
            bookmarks = []
            
        bookmarks.append({
            "position": position,
            "preview": preview
        })
        self.settings.setValue(f"bookmarks_{self.current_book_path}", bookmarks)
        QMessageBox.information(self, "成功", "书签添加成功")'''
new_add = '''    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        from datetime import datetime
        if not self.current_book_path:
            QMessageBox.warning(self, "警告", "请先打开一本书籍")
            return
        
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        preview = self.get_position_preview(pos)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not hasattr(self, 'bookmark_list'):
            self.bookmark_list = []
        
        self.bookmark_list.append({
            'position': pos,
            'preview': preview,
            'time': timestamp
        })
        self.save_bookmarks()
        self.refresh_bookmark_list()
        QMessageBox.information(self, "成功", f"书签已添加！\\n时间：{timestamp}")'''
content = content.replace(old_add, new_add)
print("✅ add_bookmark 已重写")
# ===== 2. 修复工具栏书签按钮绑定 =====
old_toolbar = '''        list_bm_action = QAction("📋 书签", self)
        toolbar.addAction(list_bm_action)'''
new_toolbar = '''        list_bm_action = QAction("📋 书签", self)
        list_bm_action.triggered.connect(self.show_bookmark_list)
        toolbar.addAction(list_bm_action)'''
content = content.replace(old_toolbar, new_toolbar)
print("✅ 工具栏书签按钮已绑定事件")
# ===== 3. 重写 refresh_bookmark_list 确保正确 =====
old_refresh = '''    def refresh_bookmark_list(self):
        """刷新书签列表（显示日期）"""
        if not hasattr(self, 'bm_list_widget'):
            return
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
# 确保 refresh 方法正确
if 'def refresh_bookmark_list' in content:
    # 找到并替换
    start = content.find('def refresh_bookmark_list')
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    old_method = content[start:end]
    # 检查是否已经正确
    if 'bookmark_list' not in old_method:
        content = content.replace(old_method, new_refresh)
        print("✅ refresh_bookmark_list 已重写")
    else:
        print("✅ refresh_bookmark_list 已正确")
# ===== 4. 重写 save_bookmarks 和 load_bookmarks =====
old_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.settings.setValue(key, getattr(self, 'bookmark_list', []))'''
new_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.settings.setValue(key, getattr(self, 'bookmark_list', []))
        elif self.current_file:
            bookmark_file = self.current_file + '.bookmarks'
            data = getattr(self, 'bookmark_list', [])
            with open(bookmark_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)'''
content = content.replace(old_save, new_save)
print("✅ save_bookmarks 已更新")
old_load = '''    def load_bookmarks(self):
        """加载书签"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            data = self.settings.value(key, [])
            self.bookmark_list = data if isinstance(data, list) else []'''
new_load = '''    def load_bookmarks(self):
        """加载书签"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            data = self.settings.value(key, [])
            self.bookmark_list = data if isinstance(data, list) else []
        elif self.current_file:
            bookmark_file = self.current_file + '.bookmarks'
            if os.path.exists(bookmark_file):
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    self.bookmark_list = json.load(f)'''
content = content.replace(old_load, new_load)
print("✅ load_bookmarks 已更新")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n🚀 所有书签代码已完整重写！")