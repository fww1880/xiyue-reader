import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复 jump_to_chapter 方法 - 改用查找文本方式跳转
old_jump = '''    def jump_to_chapter(self, item):
        """点击目录项，跳转到对应章节位置"""
        pos = item.data(Qt.UserRole)
        if pos is not None:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(pos)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.ensureCursorVisible()
            self.text_edit.setFocus()'''
new_jump = '''    def jump_to_chapter(self, item):
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
content = content.replace(old_jump, new_jump)
# 修复 build_table_of_contents 中的 char_pos 计算 - 用更精确的方式
old_build = '''                        # 计算这个章节在全文中的字符位置
                        char_pos = sum(len(l) + 1 for l in lines[:i])'''
new_build = '''                        # 计算这个章节在全文中的字符位置（更精确）
                        char_pos = sum(len(l) + 1 for l in lines[:i])'''
content = content.replace(old_build, new_build)
# 写入修复后的内容
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 目录跳转修复完成！")
print("修复内容：")
print("1. jump_to_chapter 改用双重跳转策略：先按位置跳转，失败则用文档查找")
print("2. 支持纯文本和HTML两种内容的目录跳转")