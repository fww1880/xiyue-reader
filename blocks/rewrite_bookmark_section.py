import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 切分成前半部分 + 书签部分 + 后半部分
lines = content.split('\n')
# 前半部分到 L1016: def show_bookmark_list
prefix = '\n'.join(lines[:1015]) + '\n'
# 后面从 L1117 开始
suffix = '\n' + '\n'.join(lines[1116:])
# 重新写整个书签部分
correct_bookmark_code = '''    def show_bookmark_list(self):
        """刷新书架面板中的书签列表"""
        self.refresh_bookmark_list()
    def refresh_bookmark_list(self):
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
            self.bm_list_widget.addItem(item)
    def jump_to_selected_bookmark(self, checked=None):
        """跳转到选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            return
        pos = item.data(Qt.UserRole)
        self.text_edit.moveCursor(QTextCursor.Start)
        for _ in range(pos):
            self.text_edit.moveCursor(QTextCursor.NextCharacter)
        self.text_edit.ensureCursorVisible()
    def delete_selected_bookmark(self):
        """删除选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            self.status_bar.showMessage("⚠️ 请先选择一个书签", 3000)
            return
        
        idx = item.data(Qt.UserRole + 1)
        if idx is None or idx >= len(self.bookmark_list):
            return
            
        deleted_bm = self.bookmark_list.pop(idx)
        self.save_bookmarks()
        self.refresh_bookmark_list()
        self.status_bar.showMessage(f"🗑️ 已删除书签：{deleted_bm['time']} {deleted_bm['preview'][:20]}", 3000)
'''
# 拼接回去
new_content = prefix + correct_bookmark_code + suffix
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ 书签区域代码已完全重写，缩进全部正确！")