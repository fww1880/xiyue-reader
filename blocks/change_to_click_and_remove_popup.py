import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 把双击改成单击 =====
old_double_click = '''        self.books_tree.itemDoubleClicked.connect(self.open_book_from_tree)'''
new_single_click = '''        self.books_tree.itemClicked.connect(self.open_book_from_tree)'''
content = content.replace(old_double_click, new_single_click)
# ===== 2. 去掉加载成功弹窗 =====
old_popup = '''            QMessageBox.information(self, "成功", f"成功加载文件：{os.path.basename(file_path)}")'''
new_no_popup = '''            # 去掉弹窗，直接加载'''
content = content.replace(old_popup, new_no_popup)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 修改完成！")
print("1. 书架中单击即可打开书籍（原来是双击）")
print("2. 打开书籍不再弹出成功确认弹窗")