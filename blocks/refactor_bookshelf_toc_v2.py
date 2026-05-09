import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 改造1：init_ui 中左侧书架面板集成目录 =====
old_init_ui = '''        # 左侧书架面板
        self.bookshelf_panel = QWidget()
        bookshelf_layout = QVBoxLayout(self.bookshelf_panel)
        
        self.books_tree = QTreeWidget()
        self.books_tree.setHeaderLabel("我的书架")
        self.books_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.books_tree.customContextMenuRequested.connect(self.show_bookshelf_context_menu)
        self.books_tree.itemDoubleClicked.connect(self.open_book_from_tree)
        
        bookshelf_layout.addWidget(self.books_tree)
        
        # 右侧阅读区域
        self.reading_panel = QWidget()
        reading_layout = QVBoxLayout(self.reading_panel)
        
        # 目录列表（默认隐藏）
        self.toc_list = QListWidget()
        self.toc_list.setVisible(False)
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        reading_layout.addWidget(self.toc_list)
        
        # 阅读文本区域'''
new_init_ui = '''        # 左侧书架面板（书架树 + 目录列表）
        self.bookshelf_panel = QWidget()
        bookshelf_layout = QVBoxLayout(self.bookshelf_panel)
        bookshelf_layout.setContentsMargins(0, 0, 0, 0)
        bookshelf_layout.setSpacing(0)
        
        # 书架树
        self.books_tree = QTreeWidget()
        self.books_tree.setHeaderLabel("我的书架")
        self.books_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.books_tree.customContextMenuRequested.connect(self.show_bookshelf_context_menu)
        self.books_tree.itemDoubleClicked.connect(self.open_book_from_tree)
        bookshelf_layout.addWidget(self.books_tree)
        
        # 目录标题标签（默认隐藏）
        self.toc_label = QLabel("目录")
        self.toc_label.setVisible(False)
        self.toc_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0;")
        bookshelf_layout.addWidget(self.toc_label)
        
        # 目录列表（默认隐藏，集成到书架面板）
        self.toc_list = QListWidget()
        self.toc_list.setVisible(False)
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        bookshelf_layout.addWidget(self.toc_list)
        
        # 右侧阅读区域
        self.reading_panel = QWidget()
        reading_layout = QVBoxLayout(self.reading_panel)
        
        # 阅读文本区域'''
content = content.replace(old_init_ui, new_init_ui)
# ===== 改造2：build_table_of_contents 中显示目录到书架面板 =====
old_toc_show = '''        # 填充目录列表（存储标题文本，跳转时用文档查找）
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, title)  # 存储标题文本用于查找
                self.toc_list.addItem(item)
            self.toc_list.show()
            self.toc_list.setMinimumWidth(200)
        else:
            self.toc_list.hide()'''
new_toc_show = '''        # 填充目录列表（存储标题文本，跳转时用文档查找）
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, title)  # 存储标题文本用于查找
                self.toc_list.addItem(item)
            self.toc_list.show()
            self.toc_label.show()
            self.toc_list.setMinimumWidth(200)
        else:
            self.toc_list.hide()
            self.toc_label.hide()'''
content = content.replace(old_toc_show, new_toc_show)
# ===== 改造3：open_book_from_tree 打开书时自动展示目录 =====
old_open_book = '''    def open_book_from_tree(self, item, column):
        """从书架树打开书籍"""
        file_path = item.data(0, Qt.UserRole)
        if file_path and os.path.exists(file_path):
            self.load_book(file_path)'''
new_open_book = '''    def open_book_from_tree(self, item, column):
        """从书架树打开书籍"""
        file_path = item.data(0, Qt.UserRole)
        if file_path and os.path.exists(file_path):
            self.load_book(file_path)
            # 展开书架树中该书的父节点，方便查看
            parent = item.parent()
            if parent:
                parent.setExpanded(True)'''
content = content.replace(old_open_book, new_open_book)
# ===== 改造4：调整分割窗口比例，给目录留空间 =====
old_splitter = '''        self.splitter.setSizes([300, 900])'''
new_splitter = '''        self.splitter.setSizes([350, 850])'''
content = content.replace(old_splitter, new_splitter)
# 写入修复后的内容
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("书架集成目录改造完成！")
print("改造内容：")
print("1. 左侧书架面板改为上下结构：书架树 + 目录列表")
print("2. 目录列表默认隐藏，打开书籍时自动显示")
print("3. 添加目录标题标签")
print("4. 调整分割窗口比例，给目录留空间")