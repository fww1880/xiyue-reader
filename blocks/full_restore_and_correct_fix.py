import os, re, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
backup_file = os.path.join(novel_reader_dir, 'main_backup_original.py')
# 检查是否有原始备份
if not os.path.exists(backup_file):
    # 尝试找其他备份
    for name in ['main.py.bak', 'main.py.backup', 'main_original.py']:
        candidate = os.path.join(novel_reader_dir, name)
        if os.path.exists(candidate):
            backup_file = candidate
            break
# 如果有备份，恢复
if os.path.exists(backup_file):
    print(f"📥 从 {backup_file} 恢复...")
    shutil.copy(backup_file, main_file)
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print("✅ 恢复完成")
else:
    print("❌ 没有可用备份，使用当前文件")
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
# 删除错误的嵌套函数定义（第1185行的 get_position_preview）
print("\n🔧 清理错误的嵌套函数...")
lines = content.split('\n')
cleaned_lines = []
skip_until_next_def = False
for i, line in enumerate(lines):
    # 检查是否是要删除的错误嵌套函数
    if i >= 1184 and i <= 1201 and 'def get_position_preview' in line:
        print(f"跳过错误行 {i+1}: {line[:50]}")
        skip_until_next_def = True
        continue
    if skip_until_next_def:
        if line.strip().startswith('def ') and not line.startswith('        '):
            skip_until_next_def = False
        else:
            continue
    cleaned_lines.append(line)
content = '\n'.join(cleaned_lines)
# 现在检查是否已有 get_position_preview 函数（正确的类方法）
if 'def get_position_preview(self, pos):' in content:
    print("✅ get_position_preview 已存在")
else:
    print("❌ get_position_preview 不存在，需要添加")
    # 在 refresh_bookmark_list 之前添加
    match_refresh = re.search(r'\n    def refresh_bookmark_list\(self\):', content)
    if match_refresh:
        insert_pos = match_refresh.start()
        new_get_preview = '''
    def get_position_preview(self, pos):
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
            return "位置 " + str(pos)
'''
        content = content[:insert_pos] + new_get_preview + content[insert_pos:]
        print("✅ 已添加 get_position_preview")
# 检查是否已有 add_bookmark 函数
if 'def add_bookmark(self):' in content:
    print("✅ add_bookmark 已存在")
else:
    print("❌ add_bookmark 不存在，需要添加")
    # 在 get_position_preview 之后添加
    match_preview = re.search(r'\n    def get_position_preview\(self, pos\):', content)
    if match_preview:
        # 找到 get_position_preview 的结束位置
        start = match_preview.end()
        # 找到下一个函数定义
        next_match = re.search(r'\n    def \w+\(self\):', content[start:])
        if next_match:
            insert_pos = start + next_match.start()
        else:
            insert_pos = start
        new_add_bookmark = '''
    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        try:
            from datetime import datetime
            if not hasattr(self, 'current_book_path') or not self.current_book_path:
                QMessageBox.warning(self, "警告", "请先打开一本书籍")
                return
            if not hasattr(self, 'text_edit') or not self.text_edit:
                QMessageBox.warning(self, "警告", "阅读器未初始化")
                return
            center_point = self.text_edit.viewport().rect().center()
            cursor = self.text_edit.cursorForPosition(center_point)
            pos = cursor.position()
            preview = self.get_position_preview(pos)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            if not hasattr(self, 'bookmark_list'):
                self.bookmark_list = []
            self.bookmark_list.append({'position': pos, 'preview': preview, 'time': timestamp})
            self.save_bookmarks()
            self.refresh_bookmark_list()
            if hasattr(self, 'status_bar') and self.status_bar:
                self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)
        except Exception as e:
            error_msg = f"添加书签失败：{str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(self, "错误", error_msg)
'''
        content = content[:insert_pos] + new_add_bookmark + content[insert_pos:]
        print("✅ 已添加 add_bookmark")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    lines = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+3)):
        print(f"{i+1}: {lines[i]}")