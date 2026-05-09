import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 替换右键菜单，增加导入书籍功能
old_menu = '''    def show_bookshelf_context_menu(self, position):
        """显示书架右键菜单"""
        item = self.books_tree.itemAt(position)
        menu = QMenu()
        
        if item is None:
            # 空白处右键：新建分类
            add_category_action = menu.addAction("📁 新建分类")
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if action == add_category_action:
                name, ok = QInputDialog.getText(self, "新建分类", "请输入分类名称：")
                if ok and name:
                    QTreeWidgetItem(self.books_tree, [name])
        else:
            # 选中了项目
            is_category = (item.parent() is None)
            if is_category:
                delete_cat_action = menu.addAction("🗑️ 删除分类")
            else:
                delete_book_action = menu.addAction("🗑️ 删除本书")
                
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if is_category and action == delete_cat_action:
                self.delete_selected_category()
            elif not is_category and action == delete_book_action:
                self.delete_selected_book()'''
new_menu = '''    def show_bookshelf_context_menu(self, position):
        """显示书架右键菜单"""
        item = self.books_tree.itemAt(position)
        menu = QMenu()
        
        if item is None:
            # 空白处右键：新建分类 + 导入书籍
            add_category_action = menu.addAction("📁 新建分类")
            import_file_action = menu.addAction("📂 导入书籍文件")
            import_folder_action = menu.addAction("📚 导入书籍文件夹")
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if action == add_category_action:
                name, ok = QInputDialog.getText(self, "新建分类", "请输入分类名称：")
                if ok and name:
                    QTreeWidgetItem(self.books_tree, [name])
            elif action == import_file_action:
                self.import_single_book_to_bookshelf()
            elif action == import_folder_action:
                self.import_folder()
        else:
            # 选中了项目
            is_category = (item.parent() is None)
            if is_category:
                delete_cat_action = menu.addAction("🗑️ 删除分类")
                import_file_action = menu.addAction("📂 导入书籍到本分类")
                import_folder_action = menu.addAction("📚 导入文件夹到本分类")
            else:
                delete_book_action = menu.addAction("🗑️ 删除本书")
                
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if is_category:
                if action == delete_cat_action:
                    self.delete_selected_category()
                elif action == import_file_action:
                    self.import_single_book_to_bookshelf(item)
                elif action == import_folder_action:
                    self.import_folder_to_category(item)
            elif not is_category and action == delete_book_action:
                self.delete_selected_book()'''
if old_menu in content:
    content = content.replace(old_menu, new_menu)
    print("✅ 已更新右键菜单（增加导入功能）")
else:
    print("⚠️ 未找到旧菜单，尝试查找...")
    # 打印当前菜单代码的前200字符以便调试
    idx = content.find('def show_bookshelf_context_menu')
    if idx >= 0:
        print(f"当前菜单代码：{content[idx:idx+600]}")
# 2. 添加 import_single_book_to_bookshelf 方法，放在 import_folder 方法之后
old_import_end = '''            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")
    def open_book_from_tree(self, item, column):'''
new_import_methods = '''            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")
    def import_single_book_to_bookshelf(self, category_item=None):
        """导入单本书到书架，可指定分类节点"""
        file_filters = "小说文件 (*.txt *.epub *.mobi *.pdf);;所有文件 (*.*)"
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择要导入的小说文件", "", file_filters)
        if not file_paths:
            return
        # 初始化 bookshelf_data
        if not hasattr(self, 'bookshelf_data'):
            self.bookshelf_data = {}
        if category_item is None:
            # 未指定分类，使用文件名作为分类名
            cat_name = "导入书籍"
            category_item = QTreeWidgetItem(self.books_tree, [cat_name])
            category_item.setData(0, Qt.UserRole, "__category__")
            if cat_name not in self.bookshelf_data:
                self.bookshelf_data[cat_name] = []
            books_in_category = self.bookshelf_data[cat_name]
        else:
            cat_name = category_item.text(0)
            if cat_name not in self.bookshelf_data:
                self.bookshelf_data[cat_name] = []
            books_in_category = self.bookshelf_data[cat_name]
        count = 0
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            book_item = QTreeWidgetItem(category_item, [file_name])
            book_item.setData(0, Qt.UserRole, file_path)
            books_in_category.append({'name': file_name, 'path': file_path})
            count += 1
        print(f"✅ 已导入 {count} 本书到分类「{cat_name}」")
    def import_folder_to_category(self, category_item):
        """导入文件夹到指定分类"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if not folder_path:
            return
        cat_name = category_item.text(0)
        if not hasattr(self, 'bookshelf_data'):
            self.bookshelf_data = {}
        if cat_name not in self.bookshelf_data:
            self.bookshelf_data[cat_name] = []
        books_in_category = self.bookshelf_data[cat_name]
        extensions = ['.txt', '.epub', '.mobi', '.pdf']
        total_files = 0
        for root, dirs, files in os.walk(folder_path):
            if root != folder_path:
                rel_path = os.path.relpath(root, folder_path)
                sub_category = QTreeWidgetItem(category_item, [rel_path])
                sub_category.setData(0, Qt.UserRole, "__subcategory__")
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        full_path = os.path.join(root, file)
                        book_item = QTreeWidgetItem(sub_category, [file])
                        book_item.setData(0, Qt.UserRole, full_path)
                        books_in_category.append({'name': file, 'path': full_path})
                        total_files += 1
            else:
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        full_path = os.path.join(root, file)
                        book_item = QTreeWidgetItem(category_item, [file])
                        book_item.setData(0, Qt.UserRole, full_path)
                        books_in_category.append({'name': file, 'path': full_path})
                        total_files += 1
        print(f"✅ 已导入 {total_files} 本书到分类「{cat_name}」")
    def open_book_from_tree(self, item, column):'''
if old_import_end in content:
    content = content.replace(old_import_end, new_import_methods)
    print("✅ 已添加 import_single_book_to_bookshelf 和 import_folder_to_category 方法")
else:
    print("⚠️ 未找到插入点，尝试精确查找...")
    # 找最后一行
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '已导入书架，共导入' in line and '本小说' in line:
            print(f"找到导入结束行 {i+1}: {line}")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    # 打印错误附近的行
    lines = content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        print(f"{i+1}: {repr(lines[i])}")