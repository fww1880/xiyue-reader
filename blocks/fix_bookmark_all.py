import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修复 load_bookmarks 方法，让它也刷新列表
old_load_bm = '''    def load_bookmarks(self):
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
new_load_bm = '''    def load_bookmarks(self):
        """加载书签并刷新显示"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            data = self.settings.value(key, [])
            self.bookmark_list = data if isinstance(data, list) else []
            self.refresh_bookmark_list()  # 刷新书签列表显示
        elif self.current_file:
            bookmark_file = self.current_file + '.bookmarks'
            if os.path.exists(bookmark_file):
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    self.bookmark_list = json.load(f)
                self.refresh_bookmark_list()'''
content = content.replace(old_load_bm, new_load_bm)
print("✅ 已修复 load_bookmarks 方法，加载后自动刷新显示")
# 2. 修复 load_book 方法中重复调用问题
old_load_book_bm = '''        self.current_book_path = file_path
        self.load_bookmarks()
        self.load_bookmarks()
        self.refresh_bookmark_list() # 加载书签'''
new_load_book_bm = '''        self.current_book_path = file_path
        self.load_bookmarks()  # 加载书签（包含刷新显示）'''
content = content.replace(old_load_book_bm, new_load_book_bm)
print("✅ 已修复 load_book 方法中的重复调用")
# 3. 在 restore_state 中，恢复书库后也要加载当前书籍的书签
old_restore_bm = '''        # 如果当前打开了书，加载它的书签
        if self.current_book_path:
            self.load_bookmarks()
            if hasattr(self, 'bookmark_list') and self.bookmark_list:
                print(f"✅ 已加载当前书籍的 {len(self.bookmark_list)} 个书签")
                self.refresh_bookmark_list()'''
new_restore_bm = '''        # 如果当前打开了书，加载它的书签
        if self.current_book_path:
            self.load_bookmarks()
            if hasattr(self, 'bookmark_list') and self.bookmark_list:
                print(f"✅ 已加载当前书籍的 {len(self.bookmark_list)} 个书签")'''
content = content.replace(old_restore_bm, new_restore_bm)
print("✅ 已简化 restore_state 中的书签加载（load_bookmarks 已包含刷新）")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 修改已保存！书签现在应该能正确保存和恢复了！")