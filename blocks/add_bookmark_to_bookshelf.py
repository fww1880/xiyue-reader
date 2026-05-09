import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到书架布局代码
old_layout = '''        # 目录列表
        self.toc_list = QListWidget()
        self.toc_list.itemClicked.connect(self.jump_to_toc_item)
        bookshelf_layout.addWidget(self.toc_list)
        self.bookshelf_dock.setWidget(bookshelf_widget)'''
new_layout = '''        # 目录列表
        self.toc_list = QListWidget()
        self.toc_list.itemClicked.connect(self.jump_to_toc_item)
        bookshelf_layout.addWidget(self.toc_list)
        # 书签标签
        self.bm_label = QLabel("书签")
        self.bm_label.setStyleSheet("font-weight: bold; color: #555;")
        bookshelf_layout.addWidget(self.bm_label)
        # 书签列表
        self.bm_list_widget = QListWidget()
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        bookshelf_layout.addWidget(self.bm_list_widget)
        self.bookshelf_dock.setWidget(bookshelf_widget)'''
content = content.replace(old_layout, new_layout)
print("✅ 书架面板中添加了书签标签和列表")
# 确保 refresh_bookmark_list 在加载文件时调用
if 'self.load_bookmarks()' in content and 'self.refresh_bookmark_list()' not in content.split('def open_file')[1].split('def ')[0]:
    content = content.replace('self.load_bookmarks()', 'self.load_bookmarks()\n        self.refresh_bookmark_list()')
    print("✅ 确保加载文件后刷新书签列表")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n🚀 书签栏已重新添加到书架面板！")