import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复 save_bookmarks 方法
old_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        key = "bookmarks_" + hash(self.current_book_path).__str__()
        self.settings.setValue(key, getattr(self, 'bookmark_list', []))
        # 同时保存到文件（更可靠）
        bookmark_file = self.current_file + '.bookmarks'
        data = getattr(self, 'bookmark_list', [])
        with open(bookmark_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)'''
new_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
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
if old_save in content:
    content = content.replace(old_save, new_save)
    print("✅ save_bookmarks 方法已修复")
else:
    print("⚠️ 未精确匹配 save_bookmarks，尝试查找替换...")
    # 查找 def save_bookmarks 到下一个 def 之间的内容
    save_match = re.search(r'    def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    if save_match:
        print(f"  找到 save_bookmarks 方法，长度 {len(save_match.group())}")
        content = content.replace(save_match.group(), new_save)
        print("✅ save_bookmarks 方法已替换")
# 修复 load_bookmarks 方法
old_load = '''    def load_bookmarks(self):
        """加载书签并刷新显示"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        key = "bookmarks_" + hash(self.current_book_path).__str__()
        data = self.settings.value(key, [])
        self.bookmark_list = data if isinstance(data, list) else []
        self.refresh_bookmark_list()  # 刷新书签列表显示
        # 尝试从文件加载（更可靠）
        bookmark_file = self.current_file + '.bookmarks'
        if os.path.exists(bookmark_file):
            try:
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    self.bookmark_list = json.load(f)
                self.refresh_bookmark_list()
            except Exception as e:
                print(f"⚠️ 书签文件加载失败：{e}")'''
new_load = '''    def load_bookmarks(self):
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
if old_load in content:
    content = content.replace(old_load, new_load)
    print("✅ load_bookmarks 方法已修复")
else:
    print("⚠️ 未精确匹配 load_bookmarks，尝试查找替换...")
    load_match = re.search(r'    def load_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    if load_match:
        print(f"  找到 load_bookmarks 方法，长度 {len(load_match.group())}")
        content = content.replace(load_match.group(), new_load)
        print("✅ load_bookmarks 方法已替换")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 main.py 修改已保存")
# 验证
print("\n📋 验证修改结果：")
idx = content.find('def save_bookmarks')
if idx >= 0:
    print(content[idx:idx+600])
print("---")
idx = content.find('def load_bookmarks')
if idx >= 0:
    print(content[idx:idx+600])