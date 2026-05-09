import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 替换 show_bookshelf_context_menu
old_menu = '''    def show_bookshelf_context_menu(self, position):
        """显示书架右键菜单"""
        menu = QMenu()
        add_category_action = menu.addAction("新建分类")
        menu.addSeparator()
        delete_book_action = menu.addAction("🗑️ 删除本书")
        action = menu.exec_(self.books_tree.mapToGlobal(position))
        if action == delete_book_action:
            self.delete_selected_book()
        if action == add_category_action:
            name, ok = QInputDialog.getText(self, "新建分类", "请输入分类名称：")
            if ok and name:
                QTreeWidgetItem(self.books_tree, [name])'''
new_menu = '''    def show_bookshelf_context_menu(self, position):
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
if old_menu in content:
    content = content.replace(old_menu, new_menu)
    print("✅ 已更新 show_bookshelf_context_menu")
else:
    print("⚠️ 未找到旧菜单代码，尝试正则替换...")
# 2. 添加 delete_selected_category 方法，放在 delete_selected_book 之后
delete_book_end = '''            self.status_bar.showMessage(f"🗑️ 已从书架移除：{book_name}", 3000)
    def change_theme(self, theme):'''
new_method = '''            self.status_bar.showMessage(f"🗑️ 已从书架移除：{book_name}", 3000)
    def delete_selected_category(self):
        """删除书架中选中的分类"""
        item = self.books_tree.currentItem()
        if not item or item.parent() is not None:
            return
        cat_name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除分类「{cat_name}」吗？\\n（该分类下的书籍也会从书架移除，不会删除源文件）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            root = self.books_tree.invisibleRootItem()
            root.removeChild(item)
            # 同步更新 bookshelf_data
            if hasattr(self, 'bookshelf_data') and cat_name in self.bookshelf_data:
                del self.bookshelf_data[cat_name]
            self.status_bar.showMessage(f"🗑️ 已删除分类：{cat_name}", 3000)
    def change_theme(self, theme):'''
if delete_book_end in content:
    content = content.replace(delete_book_end, new_method)
    print("✅ 已添加 delete_selected_category 方法")
else:
    print("❌ 未找到插入点")
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