import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 修改1: 书架右键菜单增加"删除书籍" =====
old_shelf_menu = """    def show_bookshelf_context_menu(self, position):
        \"\"\"显示书架右键菜单\"\"\"
        menu = QMenu()
        add_category_action = menu.addAction(\"新建分类\")
        action = menu.exec_(self.books_tree.mapToGlobal(position))"""
new_shelf_menu = """    def show_bookshelf_context_menu(self, position):
        \"\"\"显示书架右键菜单\"\"\"
        menu = QMenu()
        add_category_action = menu.addAction(\"新建分类\")
        menu.addSeparator()
        delete_book_action = menu.addAction(\"🗑️ 删除本书\")
        action = menu.exec_(self.books_tree.mapToGlobal(position))
        if action == delete_book_action:
            self.delete_selected_book()"""
if old_shelf_menu in content:
    content = content.replace(old_shelf_menu, new_shelf_menu)
    print("✅ 修改1：书架右键菜单已增加「删除本书」")
else:
    print("⚠️ 修改1：未找到书架右键菜单代码")
# ===== 修改2: 添加 delete_selected_book 方法（在 show_bookshelf_context_menu 后面）=====
# 找到 show_bookshelf_context_menu 方法的结束位置
lines = content.split('\n')
insert_pos = None
for i, line in enumerate(lines):
    if 'def show_bookshelf_context_menu' in line:
        # 找到方法结束位置（下一个 def 或类结束）
        for j in range(i+1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                insert_pos = j
                break
        break
delete_book_method = '''
    def delete_selected_book(self):
        """删除书架中选中的书籍"""
        from PyQt5.QtWidgets import QMessageBox
        item = self.books_tree.currentItem()
        if not item or not item.data(0, Qt.UserRole):
            self.status_bar.showMessage("⚠️ 请先选择一本书", 3000)
            return
        book_path = item.data(0, Qt.UserRole)
        book_name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要从书架中删除「{book_name}」吗？\\n（不会删除源文件）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 从书架树中移除
            parent = item.parent()
            if parent:
                parent.removeChild(item)
            else:
                root = self.books_tree.invisibleRootItem()
                root.removeChild(item)
            self.status_bar.showMessage(f"🗑️ 已从书架移除：{book_name}", 3000)
'''
if insert_pos:
    lines.insert(insert_pos, delete_book_method)
    content = '\n'.join(lines)
    print(f"✅ 修改2：已添加 delete_selected_book 方法")
else:
    print("⚠️ 修改2：未找到插入位置")
# ===== 修改3: 书签列表启用右键菜单 =====
# 找到 bm_list_widget 的创建位置，添加右键菜单策略
old_bm_list = """        self.bm_list_widget = QListWidget()
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        bookshelf_layout.addWidget(self.bm_list_widget)"""
new_bm_list = """        self.bm_list_widget = QListWidget()
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        self.bm_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bm_list_widget.customContextMenuRequested.connect(self.show_bookmark_context_menu)
        bookshelf_layout.addWidget(self.bm_list_widget)"""
if old_bm_list in content:
    content = content.replace(old_bm_list, new_bm_list)
    print("✅ 修改3：书签列表已启用右键菜单")
else:
    print("⚠️ 修改3：未找到书签列表创建代码")
# ===== 修改4: 添加 show_bookmark_context_menu 方法 =====
# 在 delete_selected_bookmark 方法后面添加
lines = content.split('\n')
insert_pos2 = None
for i, line in enumerate(lines):
    if 'def delete_selected_bookmark' in line:
        for j in range(i+1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                insert_pos2 = j
                break
        break
bookmark_context_method = '''
    def show_bookmark_context_menu(self, position):
        """显示书签右键菜单"""
        menu = QMenu()
        delete_action = menu.addAction("🗑️ 删除此书签")
        action = menu.exec_(self.bm_list_widget.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_bookmark()
'''
if insert_pos2:
    lines.insert(insert_pos2, bookmark_context_method)
    content = '\n'.join(lines)
    print(f"✅ 修改4：已添加 show_bookmark_context_menu 方法")
else:
    print("⚠️ 修改4：未找到插入位置")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 所有修改完成，正在验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")