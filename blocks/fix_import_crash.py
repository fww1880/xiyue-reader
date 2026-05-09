import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 修复1：import_folder 中给分类节点设置标记，防止误点击 =====
old_import = '''    def import_folder(self):
        """批量导入文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if folder_path:
            # 添加到书架
            category_name = os.path.basename(folder_path)
            category_item = QTreeWidgetItem(self.books_tree, [category_name])
            
            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                # 为子文件夹创建分类节点
                if root != folder_path:
                    rel_path = os.path.relpath(root, folder_path)
                    sub_category = QTreeWidgetItem(category_item, [rel_path])
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(sub_category, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            total_files += 1
                else:
                    # 根文件夹下的文件直接添加到主分类下
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(category_item, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            total_files += 1
                
            # 去掉导入确认弹窗，直接导入
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")'''
new_import = '''    def import_folder(self):
        """批量导入文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if folder_path:
            # 添加到书架
            category_name = os.path.basename(folder_path)
            category_item = QTreeWidgetItem(self.books_tree, [category_name])
            category_item.setData(0, Qt.UserRole, "__category__")  # 标记为分类节点
            
            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                # 为子文件夹创建分类节点
                if root != folder_path:
                    rel_path = os.path.relpath(root, folder_path)
                    sub_category = QTreeWidgetItem(category_item, [rel_path])
                    sub_category.setData(0, Qt.UserRole, "__subcategory__")  # 标记为子分类
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(sub_category, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            total_files += 1
                else:
                    # 根文件夹下的文件直接添加到主分类下
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(category_item, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            total_files += 1
                
            # 去掉导入确认弹窗，直接导入
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")'''
content = content.replace(old_import, new_import)
# ===== 修复2：open_book_from_tree 增加保护，防止点击分类节点崩溃 =====
old_open_book = '''    def open_book_from_tree(self, item, column):
        """从书架树打开书籍"""
        file_path = item.data(0, Qt.UserRole)
        if file_path and os.path.exists(file_path):
            self.load_book(file_path)
            # 展开书架树中该书的父节点，方便查看
            parent = item.parent()
            if parent:
                parent.setExpanded(True)'''
new_open_book = '''    def open_book_from_tree(self, item, column):
        """从书架树打开书籍"""
        file_path = item.data(0, Qt.UserRole)
        # 保护：跳过分类节点和无效文件
        if not file_path or file_path.startswith("__"):
            return
        if os.path.exists(file_path):
            self.load_book(file_path)
            # 展开书架树中该书的父节点，方便查看
            parent = item.parent()
            if parent:
                parent.setExpanded(True)'''
content = content.replace(old_open_book, new_open_book)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 导入闪退问题已修复！")
print("修复内容：")
print("1. 分类节点标记为 __category__，防止误点击")
print("2. 子分类节点标记为 __subcategory__，防止误点击")
print("3. open_book_from_tree 增加保护，跳过分类节点和无效文件")