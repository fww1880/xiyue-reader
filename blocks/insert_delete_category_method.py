import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找 def change_theme 的位置
insert_idx = None
for i, line in enumerate(lines):
    if line.strip() == 'def change_theme(self, theme):':
        insert_idx = i
        break
if insert_idx:
    new_method_lines = [
        '    def delete_selected_category(self):\n',
        '        """删除书架中选中的分类"""\n',
        '        item = self.books_tree.currentItem()\n',
        '        if not item or item.parent() is not None:\n',
        '            return\n',
        '        cat_name = item.text(0)\n',
        '        reply = QMessageBox.question(\n',
        '            self, "确认删除",\n',
        '            f"确定要删除分类「{cat_name}」吗？\\n（该分类下的书籍也会从书架移除，不会删除源文件）",\n',
        '            QMessageBox.Yes | QMessageBox.No,\n',
        '            QMessageBox.No\n',
        '        )\n',
        '        if reply == QMessageBox.Yes:\n',
        '            root = self.books_tree.invisibleRootItem()\n',
        '            root.removeChild(item)\n',
        '            # 同步更新 bookshelf_data\n',
        '            if hasattr(self, "bookshelf_data") and cat_name in self.bookshelf_data:\n',
        '                del self.bookshelf_data[cat_name]\n',
        '            self.status_bar.showMessage(f"🗑️ 已删除分类：{cat_name}", 3000)\n',
        '\n'
    ]
    # 插入到 change_theme 之前
    for j, ml in enumerate(new_method_lines):
        lines.insert(insert_idx + j, ml)
    print(f"✅ 已在第 {insert_idx+1} 行前插入 delete_selected_category 方法")
else:
    print("❌ 未找到插入点")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
# 语法检查
import ast
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")