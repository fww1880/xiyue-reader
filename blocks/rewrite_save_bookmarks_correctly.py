import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 删除所有 save_bookmarks 和 load_bookmarks 定义，然后重新添加正确的版本
# 先删除
content = re.sub(r'def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', '', content, flags=re.DOTALL)
content = re.sub(r'def load_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', '', content, flags=re.DOTALL)
# 找到 add_bookmark 结束位置，在后面插入正确的 save_bookmarks 和 load_bookmarks
match_add = re.search(r'(    def add_bookmark\(self\):.*?\n        except.*?QMessageBox\.critical.*?\n)', content, re.DOTALL)
if match_add:
    insert_pos = match_add.end()
    print(f"找到 add_bookmark 结束位置：{insert_pos}")
    # 正确的函数定义
    new_functions = '''
    def save_bookmarks(self):
        """保存书签到本地"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        key = "bookmarks_" + hash(self.current_book_path).__str__()
        data = getattr(self, 'bookmark_list', [])
        # 保存到文件（最可靠的方式）
        bookmark_file = self.current_book_path + '.bookmarks'
        try:
            with open(bookmark_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # 也保存到 QSettings 作为备份
            self.settings.setValue(key, data)
        except Exception as e:
            print(f"⚠️ 书签保存失败：{e}")
    def load_bookmarks(self):
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
        self.refresh_bookmark_list()
'''
    content = content[:insert_pos] + new_functions + content[insert_pos:]
    print("✅ 已插入正确的 save_bookmarks 和 load_bookmarks")
    # 保存
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("💾 已保存")
    # 语法检查
    import ast
    try:
        ast.parse(content)
        print("✅ 语法检查通过")
    except SyntaxError as e:
        print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
        lines = content.split('\n')
        for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
            print(f"{i+1:4d}: {repr(lines[i])}")
else:
    print("❌ 未找到 add_bookmark")