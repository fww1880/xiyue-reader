import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 在 restore_state 方法末尾添加加载所有书签的逻辑
old_restore_end2 = '''            print("✅ 书库已恢复")'''
new_restore_end2 = '''            print("✅ 书库已恢复")
        
        # 加载所有书籍的书签（遍历 bookshelf_data 中的所有书）
        if hasattr(self, 'bookshelf_data'):
            for category_name, books in self.bookshelf_data.items():
                for book in books:
                    book_path = book['path']
                    key = "bookmarks_" + hash(book_path).__str__()
                    bookmarks = self.settings.value(key, [])
                    if bookmarks:
                        print(f"  📑 已加载 {os.path.basename(book_path)} 的 {len(bookmarks)} 个书签")
        # 如果当前打开了书，加载它的书签
        if self.current_book_path:
            self.load_bookmarks()
            if hasattr(self, 'bookmark_list') and self.bookmark_list:
                print(f"✅ 已加载当前书籍的 {len(self.bookmark_list)} 个书签")
                self.refresh_bookmark_list()'''
content = content.replace(old_restore_end2, new_restore_end2)
print("✅ 已在 restore_state 中添加加载所有书签的逻辑")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")