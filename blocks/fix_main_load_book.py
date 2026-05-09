# 读取现有main.py
with open('novel_reader/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 找到load_book方法，加强异常处理
old_code = """    def load_book(self, file_path):
        \"\"\"加载书籍文件\"\"\"
        from file_handler import FileHandler
        handler = FileHandler()
        
        try:
            content = handler.read_file(file_path)
            self.text_edit.setPlainText(content)
            self.current_book_path = file_path
            self.setWindowTitle(f\"本地小说阅读器 - {os.path.basename(file_path)}\")
            
            # 恢复上次阅读位置
            position = self.settings.value(f\"position_{file_path}\", 0, int)
            if position > 0:
                cursor = self.text_edit.textCursor()
                cursor.setPosition(position)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                
            QMessageBox.information(self, \"成功\", f\"成功加载文件：{os.path.basename(file_path)}\")
        except Exception as e:
            QMessageBox.critical(self, \"错误\", f\"加载文件失败：{str(e)}\")"""
new_code = """    def load_book(self, file_path):
        \"\"\"加载书籍文件\"\"\"
        try:
            from file_handler import FileHandler
            handler = FileHandler()
            
            content = handler.read_file(file_path)
            self.text_edit.setPlainText(content)
            self.current_book_path = file_path
            self.setWindowTitle(f\"本地小说阅读器 - {os.path.basename(file_path)}\")
            
            # 恢复上次阅读位置
            position = self.settings.value(f\"position_{file_path}\", 0, int)
            if position > 0 and position < len(content):
                cursor = self.text_edit.textCursor()
                cursor.setPosition(position)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                
            QMessageBox.information(self, \"成功\", f\"成功加载文件：{os.path.basename(file_path)}\")
        except Exception as e:
            # 双层保护，绝对不闪退
            error_msg = f"加载文件失败：{str(e)}\\n\\n请检查文件是否存在、损坏或格式不支持。"
            try:
                QMessageBox.critical(self, "错误", error_msg)
            except:
                # 如果连弹窗都失败了，至少保证不崩溃
                print(error_msg)
            """
# 替换
new_content = content.replace(old_code, new_code)
# 写回文件
with open('novel_reader/main.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ main.py 的load_book方法已修复，异常处理加强完成！")
utils.set_state(success=True)