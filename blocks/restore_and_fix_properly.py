import os, re, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
backup_file = os.path.join(novel_reader_dir, 'main.py.bak')
# 如果有备份，先恢复
if os.path.exists(backup_file):
    print("📥 从备份恢复...")
    shutil.copy(backup_file, main_file)
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
else:
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # 创建备份
    shutil.copy(main_file, backup_file)
    print("💾 已创建备份")
# 使用 Edit 工具来精确替换 add_bookmark 函数
print("\n🔍 准备精确修复 add_bookmark 函数...")
# 找到旧的 add_bookmark 函数
old_add_pattern = r'(    def add_bookmark\(self\):\n        """添加书签.*?self\.status_bar\.showMessage\(f"✅ 书签已添加：{timestamp}", 3000\))'
match = re.search(old_add_pattern, content, re.DOTALL)
if match:
    old_func = match.group(1)
    print(f"找到旧函数，长度：{len(old_func)}")
    # 新函数（正确的缩进）
    new_func = '''    def add_bookmark(self):
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
            
            # 获取位置
            center_point = self.text_edit.viewport().rect().center()
            cursor = self.text_edit.cursorForPosition(center_point)
            pos = cursor.position()
            preview = self.get_position_preview(pos)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 初始化并添加
            if not hasattr(self, 'bookmark_list'):
                self.bookmark_list = []
            self.bookmark_list.append({'position': pos, 'preview': preview, 'time': timestamp})
            
            # 保存和刷新
            self.save_bookmarks()
            self.refresh_bookmark_list()
            self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)
        except Exception as e:
            error_msg = f"添加书签失败：{str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(self, "错误", error_msg)'''
    
    # 替换
    content = content.replace(old_func, new_func)
    print("✅ 已替换 add_bookmark")
    
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
        # 显示错误位置
        lines = content.split('\n')
        for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
            print(f"{i+1}: {lines[i]}")
else:
    print("❌ 未找到旧函数")