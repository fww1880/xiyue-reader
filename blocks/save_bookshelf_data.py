import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 在 on_close 方法中添加保存书库
old_on_close_save_bookmarks = '''        # 保存所有书签（已经在添加/删除时实时保存，这里再确保一次）
        self.save_bookmarks()
        print("✅ 所有状态已保存！")'''
new_on_close_save_bookmarks = '''        # 保存所有书签（已经在添加/删除时实时保存，这里再确保一次）
        self.save_bookmarks()
        # 保存书架中所有导入的书籍
        if hasattr(self, 'bookshelf_data'):
            self.settings.setValue("bookshelf_data", self.bookshelf_data)
            # 保存展开/折叠状态
            expanded_states = []
            root = self.books_tree.invisibleRootItem()
            for i in range(root.childCount()):
                item = root.child(i)
                expanded_states.append(item.isExpanded())
            self.settings.setValue("bookshelf_expanded", expanded_states)
        print("✅ 所有状态已保存！")'''
content = content.replace(old_on_close_save_bookmarks, new_on_close_save_bookmarks)
print("✅ 已在 on_close 中添加书库保存")
# 2. 在 restore_state 方法中添加恢复书库
old_restore_end = '''                self.text_edit.ensureCursorVisible()
                self.status_bar.showMessage(f"📖 已恢复到上次阅读进度\", 3000)'''
new_restore_end = '''                self.text_edit.ensureCursorVisible()
                self.status_bar.showMessage(f"📖 已恢复到上次阅读进度\", 3000)
        
        # 恢复书架中的所有书籍
        saved_books = self.settings.value("bookshelf_data")
        if saved_books and hasattr(self, 'books_tree'):
            # 清空现有树
            self.books_tree.clear()
            self.bookshelf_data = saved_books
            # 重建书架树
            for folder_name, book_list in self.bookshelf_data.items():
                folder_item = QTreeWidgetItem(self.books_tree, [folder_name])
                for book in book_list:
                    book_item = QTreeWidgetItem(folder_item, [book['name']])
                    book_item.setData(0, Qt.UserRole, book['path'])
            # 恢复展开/折叠状态
            expanded_states = self.settings.value("bookshelf_expanded")
            if expanded_states:
                root = self.books_tree.invisibleRootItem()
                for i in range(root.childCount()):
                    item = root.child(i)
                    if i < len(expanded_states):
                        item.setExpanded(bool(expanded_states[i]))
            print("✅ 书库已恢复")'''
content = content.replace(old_restore_end, new_restore_end)
print("✅ 已在 restore_state 中添加书库恢复")
# 3. 检查 bookshelf_data 是否在 __init__ 中初始化
if 'self.bookshelf_data = []' not in content and 'self.bookshelf_data = {}' not in content:
    # 在 import_folder 附近添加初始化
    if 'self.bookshelf_data = {' not in content:
        # 查找 init_ui 中 books_tree 初始化位置
        old_books_init = '''# 书架树
self.books_tree = QTreeWidget()
self.books_tree.setHeaderLabel("书架")'''
        new_books_init = '''# 书架树
self.books_tree = QTreeWidget()
self.books_tree.setHeaderLabel("书架")
self.bookshelf_data = {}  # 存储书架中的书籍数据: {文件夹名称: [{name, path}, ...]}'''
        content = content.replace(old_books_init, new_books_init)
        print("✅ 已添加 bookshelf_data 初始化")
else:
    print("✅ bookshelf_data 已经初始化")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 修改已保存！现在书库和书签都会永久保存，关闭再打开也不会丢失！")