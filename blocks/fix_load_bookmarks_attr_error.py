import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 load_bookmarks 函数并修复
old_load_bm = '''    def load_bookmarks(self):
        """加载书签并刷新显示（优先从文件加载，更可靠）"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        self.bookmark_list = []
        # 优先从文件加载（最可靠）
        bookmark_file = self.current_file + '.bookmarks'
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
new_load_bm = '''    def load_bookmarks(self):
        """加载书签并刷新显示（优先从文件加载，更可靠）"""
        # 确保 current_file 和 current_book_path 都已初始化
        if not hasattr(self, 'current_file') or not self.current_file:
            return
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        self.bookmark_list = []
        # 优先从文件加载（最可靠）
        bookmark_file = self.current_file + '.bookmarks'
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
if old_load_bm in content:
    content = content.replace(old_load_bm, new_load_bm)
    print("✅ load_bookmarks 已修复：添加了 current_file 属性检查")
else:
    print("⚠️ 未精确匹配，尝试模糊修复...")
    # 查找 def load_bookmarks 到下一个 def 之间的内容
    match = re.search(r'def load_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    if match:
        old_func = match.group()
        # 在函数开头添加 current_file 检查
        if 'if not hasattr(self, \'current_file\')' not in old_func:
            # 找到第一个 return 或第一个逻辑判断
            lines = old_func.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if 'def load_bookmarks' in line:
                    # 在 docstring 后添加检查
                    pass
            # 简单替换：在函数体开始处添加检查
            new_func = old_func.replace(
                'if not hasattr(self, \'current_book_path\')',
                'if not hasattr(self, \'current_file\') or not self.current_file:\n            return\n        if not hasattr(self, \'current_book_path\')'
            )
            content = content.replace(old_func, new_func)
            print("✅ 已模糊修复：添加 current_file 检查")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ Python 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
# 验证
idx = content.find('def load_bookmarks')
if idx >= 0:
    end = idx + 400
    print("\n📋 修复后的 load_bookmarks 开头：")
    print(content[idx:end])