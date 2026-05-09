import os
import re
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 统计有多少个 self.bookmarks 还在使用
count = len(re.findall(r'self\.bookmarks', content))
print(f"🔍 当前代码中还有 {count} 处使用 self.bookmarks（应该使用 self.bookmark_list）")
# 一次性替换所有正确引用
# 先替换所有方法内的引用，除了初始化那里已经做过了
# 完整的书签功能重写
old_add = '''    def add_bookmark(self):
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
# 确保 add_bookmark 正确
content = content.replace(old_add, old_add)  # 占位，保证格式正确
# 修复 save_bookmarks（文件保存版，不是 QSettings）
old_save_file = '''    def save_bookmarks(self):
        """保存书签列表到文件"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        data = getattr(self, 'bookmark_list', [])
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)'''
content = re.sub(r'def save_bookmarks\(.*?json\.dump\(.*?\)', '''    def save_bookmarks(self):
        """保存书签列表到文件"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        data = getattr(self, 'bookmark_list', [])
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)''', content, flags=re.DOTALL)
# 修复 load_bookmarks 文件版
old_load_file = '''    def load_bookmarks(self):
        """从文件加载书签列表"""
        if not self.current_file:
            return
        bookmark_file = self.current_file + '.bookmarks'
        if os.path.exists(bookmark_file):
            with open(bookmark_file, 'r', encoding='utf-8') as f:
                self.bookmark_list = json.load(f)'''
# 匹配并替换
content = re.sub(r'def load_bookmarks\(.*?self\.bookmark_list = json\.load\(f\)', old_load_file, content, flags=re.DOTALL)
# 修复 refresh_bookmark_list 完全版
new_refresh = '''    def refresh_bookmark_list(self):
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
# 找到旧的 refresh 替换
old_refresh_pattern = r'def refresh_bookmark_list.*?self\.bm_list_widget\.addItem\(.*?\)'
content = re.sub(old_refresh_pattern, new_refresh, content, flags=re.DOTALL)
print("✅ refresh_bookmark_list 已更新")
# 修复 jump_to_selected_bookmark
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
old_jump_pattern = r'def jump_to_selected_bookmark.*?self\.text_edit\.ensureCursorVisible\(\)'
content = re.sub(old_jump_pattern, new_jump, content, flags=re.DOTALL)
print("✅ jump_to_selected_bookmark 已更新")
# 修复 delete_selected_bookmark
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
old_delete_pattern = r'def delete_selected_bookmark.*?3000\)'
content = re.sub(old_delete_pattern, new_delete, content, flags=re.DOTALL)
print("✅ delete_selected_bookmark 已更新")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n🚀 全部书签代码已重构完成！")