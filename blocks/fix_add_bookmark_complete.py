import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 add_bookmark 函数
print("🔍 定位 add_bookmark 函数...")
match = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    old_func = match.group()
    print(f"当前代码长度：{len(old_func)}")
    # 创建新的 add_bookmark 函数，添加完整的检查和 try-except
    new_func = '''    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        try:
            from datetime import datetime
            
            # 完整检查：确保所有必要的属性都存在
            if not hasattr(self, 'current_book_path') or not self.current_book_path:
                QMessageBox.warning(self, "警告", "请先打开一本书籍")
                return
            
            if not hasattr(self, 'text_edit') or not self.text_edit:
                QMessageBox.warning(self, "警告", "阅读器未初始化，请重启程序")
                return
            
            if not hasattr(self, 'status_bar') or not self.status_bar:
                QMessageBox.warning(self, "警告", "状态栏未初始化")
                return
            
            # 获取当前视口中心位置的字符索引
            center_point = self.text_edit.viewport().rect().center()
            cursor = self.text_edit.cursorForPosition(center_point)
            pos = cursor.position()
            
            # 获取预览文本
            preview = self.get_position_preview(pos)
            
            # 生成时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 初始化书签列表
            if not hasattr(self, 'bookmark_list'):
                self.bookmark_list = []
            
            # 添加书签
            self.bookmark_list.append({
                'position': pos,
                'preview': preview,
                'time': timestamp
            })
            
            # 保存书签
            self.save_bookmarks()
            
            # 刷新书签列表显示
            self.refresh_bookmark_list()
            
            # 显示提示
            self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)
            
        except Exception as e:
            # 捕获所有异常，避免闪退
            error_msg = f"添加书签失败：{str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(self, "错误", error_msg)'''
    
    # 替换旧函数
    content = content.replace(old_func, new_func)
    print("✅ 已替换 add_bookmark 函数")
    
    # 同时修复 get_position_preview，添加检查
    print("\n🔍 修复 get_position_preview 函数...")
    match_preview = re.search(r'def get_position_preview\(self, pos\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    if match_preview:
        old_preview = match_preview.group()
        new_preview = '''    def get_position_preview(self, pos):
        """获取位置附近的文本预览"""
        try:
            if not hasattr(self, 'text_edit') or not self.text_edit:
                return "位置 " + str(pos)
            
            cursor = self.text_edit.textCursor()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            preview = cursor.selectedText().strip()
            if len(preview) > 50:
                preview = preview[:50]
            return preview if preview else "位置 " + str(pos)
        except Exception as e:
            print(f"⚠️ get_position_preview 错误：{e}")
            return "位置 " + str(pos)'''
        content = content.replace(old_preview, new_preview)
        print("✅ 已替换 get_position_preview 函数")
    
    # 保存修改
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n💾 修改已保存")
    
    # 语法检查
    import ast
    try:
        ast.parse(content)
        print("✅ Python 语法检查通过")
    except SyntaxError as e:
        print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    
    # 验证
    print("\n📋 验证修复：")
    if 'try:' in content[content.find('def add_bookmark'):content.find('def add_bookmark')+500]:
        print("✅ add_bookmark 添加了 try-except")
    if 'hasattr(self, \'text_edit\')' in content[content.find('def add_bookmark'):content.find('def add_bookmark')+500]:
        print("✅ add_bookmark 添加了 text_edit 检查")