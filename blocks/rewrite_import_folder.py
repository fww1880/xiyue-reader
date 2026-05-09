import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 import_folder 方法并完整替换
old_method_start = '''    def import_folder(self):
        """批量导入文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if folder_path:
            # 添加到书架
            category_name = os.path.basename(folder_path)
            category_item = QTreeWidgetItem(self.books_tree, [category_name])
            category_item.setData(0, Qt.UserRole, "__category__")
            category_item.setData(0, Qt.UserRole, "__category__")  # 标记为分类节点
            
            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                # 为子文件夹创建分类节点
                if root != folder_path:
                    rel_path = os.path.relpath(root, folder_path)
                    sub_category = QTreeWidgetItem(category_item, [rel_path])
                    sub_category.setData(0, Qt.UserRole, "__subcategory__")
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
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")
            # 保存到 bookshelf_data
            if not hasattr(self, 'bookshelf_data'):
                self.bookshelf_data = {}
            # TODO: 需要重构以正确存储嵌套结构'''
new_method = '''    def import_folder(self):
        """批量导入文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if folder_path:
            # 初始化 bookshelf_data
            if not hasattr(self, 'bookshelf_data'):
                self.bookshelf_data = {}
            
            # 添加到书架
            category_name = os.path.basename(folder_path)
            category_item = QTreeWidgetItem(self.books_tree, [category_name])
            category_item.setData(0, Qt.UserRole, "__category__")
            
            # 存储这个分类下的所有书籍
            books_in_category = []
            
            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                # 为子文件夹创建分类节点
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
                    # 根文件夹下的文件直接添加到主分类下
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(category_item, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            books_in_category.append({'name': file, 'path': full_path})
                            total_files += 1
            
            # 保存到 bookshelf_data
            self.bookshelf_data[category_name] = books_in_category
            
            # 去掉导入确认弹窗，直接导入
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")'''
if old_method_start in content:
    content = content.replace(old_method_start, new_method)
    print("✅ 已完整替换 import_folder 方法，现在会正确保存书库数据")
else:
    print("⚠️ 未找到完全匹配的旧代码，尝试定位方法体替换...")
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if 'def import_folder(self):' in line:
            start_idx = i
        if start_idx is not None and i > start_idx:
            if line.strip().startswith('def ') and 'import_folder' not in line:
                end_idx = i
                break
    if start_idx and end_idx:
        # 替换从 start_idx 到 end_idx 的内容
        new_lines = new_method.split('\n')
        content = '\n'.join(lines[:start_idx] + new_lines + lines[end_idx:])
        print(f"✅ 已按行替换 import_folder 方法（L{start_idx+1}-L{end_idx}）")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")