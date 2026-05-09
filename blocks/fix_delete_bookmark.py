import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复删除方法
old_delete = '''    def delete_selected_bookmark(self):
        """删除选中的书签"""
        current_row = self.bm_list_widget.currentRow()
        if current_row == -1:
            self.status_bar.showMessage("⚠️ 请先选择一个书签", 3000)
            return
        
        bm = self.bookmarks.pop(current_row)
        self.save_bookmarks()
        self.refresh_bookmark_list()
        self.status_bar.showMessage(f"🗑️ 已删除书签：{bm['title']}", 3000)'''
new_delete = '''    def delete_selected_bookmark(self):
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
        self.status_bar.showMessage(f"🗑️ 已删除书签：{deleted_bm['time']} {deleted_bm['preview'][:20]}", 3000)'''
content = content.replace(old_delete, new_delete)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 书签删除方法已修复！")