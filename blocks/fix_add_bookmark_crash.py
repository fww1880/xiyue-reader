import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 add_bookmark 函数
print("🔍 检查 add_bookmark 函数...")
match = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    print(f"📄 当前 add_bookmark 代码长度：{len(match.group())}")
    old_func = match.group()
    print(f"\n代码片段：\n{old_func[:500]}...")
    # 检查是否访问了 current_file，如果没有检查会闪退
    if 'self.current_file' in old_func and 'hasattr' not in old_func[:old_func.find('self.save_bookmarks()')]:
        print("\n⚠️ 发现问题：add_bookmark 调用 save_bookmarks → save_bookmarks 又调用 load_bookmarks，但是没有检查 current_file")
        # 修复 add_bookmark：确保 current_file 存在
        new_func = '''    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        if not hasattr(self, 'current_file') or not self.current_file:
            self.status_bar.showMessage("⚠️ 请先打开小说文件再添加书签", 3000)
            return
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            self.status_bar.showMessage("⚠️ 请先打开小说文件再添加书签", 3000)
            return
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        block = cursor.block()
        line_number = block.blockNumber() + 1
        # 获取当前位置上下文（预览）
        start_block = block.previous() if block.previous().isValid() else block
        preview = ""
        for i in range(3):
            if start_block.isValid():
                preview += start_block.text() + " "
                start_block = start_block.next()
        preview = preview.strip()
        if not preview:
            preview = "开始位置"
        # 获取当前时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not hasattr(self, 'bookmark_list'):
            self.bookmark_list = []
        self.bookmark_list.append({
            "position": position,
            "line": line_number,
            "time": timestamp,
            "preview": preview
        })
        self.save_bookmarks()
        self.refresh_bookmark_list()
        self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)'''
        content = content.replace(old_func, new_func)
        print("✅ 已修复 add_bookmark：添加了 current_file 存在性检查")
# 检查 save_bookmarks 是否也需要检查
print("\n🔍 检查 save_bookmarks 函数...")
match_sv = re.search(r'def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_sv:
    old_sv = match_sv.group()
    if 'current_file' in old_sv and 'if not hasattr' not in old_sv:
        print("⚠️ save_bookmarks 缺少 current_file 检查，修复...")
        new_sv = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if not hasattr(self, 'current_file') or not self.current_file:
            return
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        key = "bookmarks_" + hash(self.current_book_path).__str__()
        data = getattr(self, 'bookmark_list', [])
        # 保存到文件（最可靠的方式）
        bookmark_file = self.current_file + '.bookmarks'
        try:
            with open(bookmark_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # 也保存到 QSettings 作为备份
            self.settings.setValue(key, data)
        except Exception as e:
            print(f"⚠️ 书签保存失败：{e}")'''
        content = content.replace(old_sv, new_sv)
        print("✅ 已修复 save_bookmarks：添加了 current_file 检查")
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
print("\n📋 验证：")
idx = content.find('def add_bookmark')
if idx >= 0:
    end = idx + 300
    print(content[idx:end])