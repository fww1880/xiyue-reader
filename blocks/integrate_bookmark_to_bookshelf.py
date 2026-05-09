import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 在书架面板中添加书签区域 =====
old_bookshelf_layout = '''        # 目录列表
        self.toc_list = QListWidget()
        self.toc_list.itemClicked.connect(self.jump_to_toc_item)
        bookshelf_layout.addWidget(self.toc_list)
        self.bookshelf_dock.setWidget(bookshelf_widget)'''
new_bookshelf_layout = '''        # 目录列表
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
content = content.replace(old_bookshelf_layout, new_bookshelf_layout)
# ===== 2. 修改 show_bookmark_list 方法，不再弹窗，改为刷新 =====
old_show_bm = '''    def show_bookmark_list(self):
        """显示书签管理窗口"""
        if not hasattr(self, 'bm_list_widget'):
            return
        # 如果已经存在窗口则刷新
        if hasattr(self, 'bookmark_dialog') and self.bookmark_dialog:
            self.bookmark_dialog.refresh_list()
            self.bookmark_dialog.show()
            return
        self.bookmark_dialog = QDialog(self)
        self.bookmark_dialog.setWindowTitle("书签管理")
        self.bookmark_dialog.resize(400, 500)
        layout = QVBoxLayout(self.bookmark_dialog)
        self.bm_list_widget = QListWidget()
        self.refresh_bookmark_list()
        # 单击即可跳转
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        layout.addWidget(self.bm_list_widget)
        btn_layout = QHBoxLayout()
        jump_btn = QPushButton("跳转到")
        jump_btn.clicked.connect(self.jump_to_selected_bookmark)
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_selected_bookmark)
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.bookmark_dialog.close)
        btn_layout.addWidget(jump_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        self.bookmark_dialog.show()'''
new_show_bm = '''    def show_bookmark_list(self):
        """刷新书架面板中的书签列表"""
        self.refresh_bookmark_list()'''
content = content.replace(old_show_bm, new_show_bm)
# ===== 3. 修改右键菜单中的"管理书签"为"刷新书签" =====
content = content.replace('list_bm_action = menu.addAction("📋 管理书签")', 'list_bm_action = menu.addAction("🔄 刷新书签列表")')
# ===== 4. 确保初始化时加载书签 =====
# 在 open_file 或 init 中确保调用 load_bookmarks 和 refresh_bookmark_list
# 检查 open_file 方法
if 'self.load_bookmarks()' in content and 'self.refresh_bookmark_list()' not in content.split('def open_file')[1].split('def ')[0]:
    # 在 open_file 的 load_bookmarks 后添加 refresh
    content = content.replace('self.load_bookmarks()', 'self.load_bookmarks()\n        self.refresh_bookmark_list()')
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 书签栏已成功集成到'我的书架'面板中！")