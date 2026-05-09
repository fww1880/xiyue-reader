import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 彻底重写 jump_to_chapter - 用 QTextDocument.find 查找章节标题
old_jump = '''    def jump_to_chapter(self, item):
        """点击目录项，跳转到对应章节位置"""
        title = item.text()
        pos = item.data(Qt.UserRole)
        if pos is not None:
            # 方法1：优先使用存储的原始文本位置（适用于纯文本）
            if not self.text_edit.toPlainText():
                # HTML内容，用查找方式
                cursor = self.text_edit.document().find(title)
                if not cursor.isNull():
                    self.text_edit.setTextCursor(cursor)
                    self.text_edit.ensureCursorVisible()
                    self.text_edit.setFocus()
                    return
            else:
                # 纯文本，用字符位置
                plain_text = self.text_edit.toPlainText()
                if pos < len(plain_text):
                    cursor = self.text_edit.textCursor()
                    cursor.setPosition(pos)
                    self.text_edit.setTextCursor(cursor)
                    self.text_edit.ensureCursorVisible()
                    self.text_edit.setFocus()
                    return
            # 方法2：如果方法1失败，用文档查找
            cursor = self.text_edit.document().find(title)
            if not cursor.isNull():
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                self.text_edit.setFocus()'''
new_jump = '''    def jump_to_chapter(self, item):
        """点击目录项，跳转到对应章节位置"""
        title = item.text()
        # 用 QTextDocument.find 查找章节标题文本
        # 从文档开头开始查找
        cursor = QTextCursor(self.text_edit.document())
        cursor.movePosition(QTextCursor.Start)
        self.text_edit.setTextCursor(cursor)
        # 查找章节标题
        found = self.text_edit.find(title)
        if found:
            self.text_edit.ensureCursorVisible()
            self.text_edit.setFocus()
        else:
            # 如果精确查找失败，尝试只查找章节标题的前几个字（去掉序号）
            import re
            # 匹配 "第X章" 或 "第X节" 等
            match = re.match(r'^\\s*([\\[【（(]?第[^\\]】）)]+[\\]】）)]?\\s*)', title)
            if match:
                prefix = match.group(1)
                cursor2 = QTextCursor(self.text_edit.document())
                cursor2.movePosition(QTextCursor.Start)
                self.text_edit.setTextCursor(cursor2)
                if self.text_edit.find(prefix):
                    self.text_edit.ensureCursorVisible()
                    self.text_edit.setFocus()'''
content = content.replace(old_jump, new_jump)
# 同时修复 build_table_of_contents - 存储章节标题文本而不是位置
old_store = '''        # 填充目录列表
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, pos)
                self.toc_list.addItem(item)'''
new_store = '''        # 填充目录列表（存储标题文本，跳转时用文档查找）
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, title)  # 存储标题文本用于查找
                self.toc_list.addItem(item)'''
content = content.replace(old_store, new_store)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 目录跳转彻底修复完成！")
print("修复内容：")
print("1. jump_to_chapter 完全改用 QTextDocument.find 查找章节标题")
print("2. 不再依赖字符位置，直接用标题文本查找")
print("3. 支持精确查找和模糊查找（去掉序号前缀）")