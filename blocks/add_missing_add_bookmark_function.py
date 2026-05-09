import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 refresh_bookmark_list 函数的位置，在它前面插入 add_bookmark
print("🔍 定位 refresh_bookmark_list 函数...")
match_refresh = re.search(r'\n    def refresh_bookmark_list\(self\):', content)
if match_refresh:
    insert_pos = match_refresh.start()
    print(f"找到位置：{insert_pos}")
    
    # 新的 add_bookmark 函数（带完整错误处理）
    new_function = '''
    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        try:
            from datetime import datetime
            
            # 完整检查
            if not hasattr(self, 'current_book_path') or not self.current_book_path:
                QMessageBox.warning(self, "警告", "请先打开一本书籍")
                return
            
            if not hasattr(self, 'text_edit') or not self.text_edit:
                QMessageBox.warning(self, "警告", "阅读器未初始化")
                return
            
            # 获取当前视口中心位置
            center_point = self.text_edit.viewport().rect().center()
            cursor = self.text_edit.cursorForPosition(center_point)
            pos = cursor.position()
            
            # 获取预览
            preview = self.get_position_preview(pos) if hasattr(self, 'get_position_preview') else "位置 " + str(pos)
            
            # 时间戳
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
            
            # 保存
            self.save_bookmarks()
            
            # 刷新显示
            self.refresh_bookmark_list()
            
            # 提示
            if hasattr(self, 'status_bar') and self.status_bar:
                self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)
                
        except Exception as e:
            error_msg = f"添加书签失败：{str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(self, "错误", error_msg)
'''
    
    # 插入新函数
    content = content[:insert_pos] + new_function + content[insert_pos:]
    
    # 保存
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已添加 add_bookmark 函数")
    
    # 语法检查
    import ast
    try:
        ast.parse(content)
        print("✅ 语法检查通过")
    except SyntaxError as e:
        print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    
    # 验证
    if 'def add_bookmark(self):' in content:
        print("✅ add_bookmark 函数已成功添加")
    else:
        print("❌ 添加失败")
else:
    print("❌ 未找到 refresh_bookmark_list 函数")