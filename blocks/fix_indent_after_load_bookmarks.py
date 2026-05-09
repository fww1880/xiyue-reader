import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 检查 1400-1420 行
print("🔍 检查 1400-1420 行:")
for i in range(1400, min(1420, len(lines))):
    print(f"{i+1:4d}: {repr(lines[i])}")
# 修复：load_bookmarks 替换后缩进错误，重新读取完整文件修复
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到完整的 load_bookmarks 函数
match = re.search(r'def load_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    old_load = match.group()
    print(f"\n当前 load_bookmarks 长度：{len(old_load)}")
    # 正确的修复版本（正确缩进）
    new_load = '''    def load_bookmarks(self):
        """加载书签并刷新显示（优先从文件加载，更可靠）"""
        # 确保 current_book_path 已初始化
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        self.bookmark_list = []
        # 优先从文件加载（最可靠）
        bookmark_file = self.current_book_path + '.bookmarks'
        if os.path.exists(bookmark_file):
            try:
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                if isinstance(file_data, list) and len(file_data) > 0:
                    self.bookmark_list = file_data
            except Exception as e:
                print(f"⚠️ 书签文件加载失败：{e}")
        # 如果文件没有数据，尝试从 QSettings 加载（备份）
        if not self.bookmark_list:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            data = self.settings.value(key, [])
            self.bookmark_list = data if isinstance(data, list) else []
        self.refresh_bookmark_list()'''
    # 替换
    content = content.replace(old_load, new_load)
    # 保存
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已修复 load_bookmarks 缩进")
    # 语法检查
    import ast
    try:
        ast.parse(content)
        print("✅ 语法检查通过")
    except SyntaxError as e:
        print(f"❌ 语法错误：{e} 第 {e.lineno} 行")