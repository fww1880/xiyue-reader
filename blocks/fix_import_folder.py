import os
import sys
# 读取 main.py
main_path = os.path.join(os.getcwd(), 'novel_reader', 'main.py')
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 修改 import_folder 方法，去掉 break，遍历所有子文件夹
old_import = """            # 遍历文件夹中的小说文件
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        full_path = os.path.join(root, file)
                        book_item = QTreeWidgetItem(category_item, [file])
                        book_item.setData(0, Qt.UserRole, full_path)
                break  # 只导入第一层"""
new_import = """            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
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
                            total_files += 1"""
content = content.replace(old_import, new_import)
# 更新提示消息，显示导入总数
old_msg = """            QMessageBox.information(self, \"导入完成\", f\"文件夹 {category_name} 已导入书架\")"""
new_msg = """            QMessageBox.information(self, \"导入完成\", f\"文件夹 {category_name} 已导入书架\\n共导入 {total_files} 本小说\")"""
content = content.replace(old_msg, new_msg)
# 写入文件
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ import_folder 修改完成！")
print("修改内容：")
print("1. 移除 break 限制，支持递归遍历所有子文件夹")
print("2. 自动为子文件夹创建树节点，层级清晰")
print("3. 导入完成后显示总导入数量")