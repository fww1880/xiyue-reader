import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 修复 refresh_bookmark_list 方法 =====
old_refresh = '''    def refresh_bookmark_list(self):
        """刷新书签列表显示"""
        self.bm_list_widget.clear()
        for i, bm in enumerate(self.bookmarks):
            display_text = f"{i+1}. {bm['title']} - {bm['preview']}... ({bm['time']})"
            item = self.bm_list_widget.addItem(display_text)'''
new_refresh = '''    def refresh_bookmark_list(self):
        """刷新书签列表显示"""
        self.bm_list_widget.clear()
        if not hasattr(self, 'bookmark_list') or not self.bookmark_list:
            return  # 没有书签时直接返回，防止报错
        for i, bm in enumerate(self.bookmark_list):
            preview = bm.get('preview', '')[:30]
            time_str = bm.get('time', '')
            display_text = f"[{time_str}] {preview}..."
            self.bm_list_widget.addItem(display_text)'''
content = content.replace(old_refresh, new_refresh)
print("✅ refresh_bookmark_list 方法已修复")
# ===== 2. 确保 __init__ 中初始化 bookmark_list =====
if 'self.bookmark_list = []' not in content:
    # 在 __init__ 中添加初始化
    init_pos = content.find('def __init__(self')
    if init_pos != -1:
        # 找到第一个方法定义前插入
        next_method = content.find('\n    def ', init_pos + 15)
        insert_code = '\n        # 书签列表\n        self.bookmark_list = []\n'
        content = content[:next_method] + insert_code + content[next_method:]
        print("✅ 已在 __init__ 中添加 bookmark_list 初始化")
# ===== 3. 统一数据结构：确保 load_bookmarks 使用 bookmark_list =====
old_load = '''    def load_bookmarks(self):
        """加载书签"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.bookmarks = self.settings.value(key, [])
            if not isinstance(self.bookmarks, list):
                self.bookmarks = []'''
new_load = '''    def load_bookmarks(self):
        """加载书签"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            data = self.settings.value(key, [])
            self.bookmark_list = data if isinstance(data, list) else []'''
content = content.replace(old_load, new_load)
print("✅ load_bookmarks 方法已适配")
# ===== 4. 统一 save_bookmarks =====
old_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.settings.setValue(key, self.bookmarks)'''
new_save = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if self.current_book_path:
            key = "bookmarks_" + hash(self.current_book_path).__str__()
            self.settings.setValue(key, getattr(self, 'bookmark_list', []))'''
content = content.replace(old_save, new_save)
print("✅ save_bookmarks 方法已适配")
# 保存文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n🚀 所有修复完成！")