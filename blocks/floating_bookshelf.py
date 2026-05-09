import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 修改导入，添加 QDockWidget =====
old_imports = '''from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QMenu,
    QToolBar, QStatusBar, QAction, QFileDialog, QMessageBox, QColorDialog,
    QSpinBox, QDoubleSpinBox, QLabel, QGroupBox, QCheckBox, QRadioButton,
    QScrollArea, QSplitter, QInputDialog, QListWidget, QListWidgetItem,
    QDialog, QDialogButtonBox
)'''
new_imports = '''from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QMenu,
    QToolBar, QStatusBar, QAction, QFileDialog, QMessageBox, QColorDialog,
    QSpinBox, QDoubleSpinBox, QLabel, QGroupBox, QCheckBox, QRadioButton,
    QScrollArea, QSplitter, QInputDialog, QListWidget, QListWidgetItem,
    QDialog, QDialogButtonBox, QDockWidget
)'''
content = content.replace(old_imports, new_imports)
# ===== 2. 修改 __init__，移除旧的 bookshelf_panel 初始化 =====
old_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.toc_list = QListWidget()
        self.toc_label = QLabel("目录")
        self.chapter_positions = []
        
        # 初始化 UI
        self.init_ui()'''
new_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.chapter_positions = []
        
        # 初始化 UI
        self.init_ui()'''
content = content.replace(old_init_vars, new_init_vars)
# ===== 3. 重写 init_ui，使用 QDockWidget =====
old_init_ui = '''    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("本地小说阅读器")
        self.setMinimumSize(1200, 800)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建分割窗口
        self.splitter = QSplitter(Qt.Horizontal)
        
        # 左侧书架面板（书架树 + 目录列表）
        self.bookshelf_panel = QWidget()
        bookshelf_layout = QVBoxLayout(self.bookshelf_panel)
        bookshelf_layout.setContentsMargins(0, 0, 0, 0)
        bookshelf_layout.setSpacing(0)
        
        # 书架树
        self.books_tree = QTreeWidget()
        self.books_tree.setHeaderLabel("我的书架")
        self.books_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.books_tree.customContextMenuRequested.connect(self.show_bookshelf_context_menu)
        self.books_tree.itemClicked.connect(self.open_book_from_tree)
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
        
        # 阅读文本区域
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.cursorPositionChanged.connect(self.update_position)
        reading_layout.addWidget(self.text_edit)
        
        # 添加到分割窗口
        self.splitter.addWidget(self.bookshelf_panel)
        self.splitter.addWidget(self.reading_panel)
        self.splitter.setSizes([350, 850])
        
        self.setCentralWidget(self.splitter)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.position_label = QLabel("进度：0%")
        self.status_bar.addWidget(self.position_label)
        self.setStatusBar(self.status_bar)
        
        # 启用键盘快捷键
        self.text_edit.keyPressEvent = self.keyboard_pagination
        
        # 自动滚屏定时器
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.do_auto_scroll)'''
new_init_ui = '''    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("本地小说阅读器")
        self.setMinimumSize(1200, 800)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # ===== 创建浮动书架窗口（QDockWidget）=====
        self.bookshelf_dock = QDockWidget("我的书架", self)
        self.bookshelf_dock.setObjectName("BookshelfDock")
        self.bookshelf_dock.setFeatures(QDockWidget.DockWidgetMovable | 
                                        QDockWidget.DockWidgetFloatable | 
                                        QDockWidget.DockWidgetClosable)
        
        # 书架内容容器
        bookshelf_widget = QWidget()
        bookshelf_layout = QVBoxLayout(bookshelf_widget)
        bookshelf_layout.setContentsMargins(5, 5, 5, 5)
        bookshelf_layout.setSpacing(5)
        
        # 书架树
        self.books_tree = QTreeWidget()
        self.books_tree.setHeaderLabel("书架")
        self.books_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.books_tree.customContextMenuRequested.connect(self.show_bookshelf_context_menu)
        self.books_tree.itemClicked.connect(self.open_book_from_tree)
        bookshelf_layout.addWidget(self.books_tree)
        
        # 目录标题
        self.toc_label = QLabel("目录")
        self.toc_label.setVisible(False)
        self.toc_label.setStyleSheet("font-weight: bold; padding: 3px; background-color: #e0e0e0; border-radius: 3px;")
        bookshelf_layout.addWidget(self.toc_label)
        
        # 目录列表
        self.toc_list = QListWidget()
        self.toc_list.setVisible(False)
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        bookshelf_layout.addWidget(self.toc_list)
        
        self.bookshelf_dock.setWidget(bookshelf_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.bookshelf_dock)
        
        # ===== 创建中央阅读区域 =====
        self.reading_panel = QWidget()
        reading_layout = QVBoxLayout(self.reading_panel)
        reading_layout.setContentsMargins(0, 0, 0, 0)
        
        # 阅读文本区域
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.cursorPositionChanged.connect(self.update_position)
        reading_layout.addWidget(self.text_edit)
        
        self.setCentralWidget(self.reading_panel)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.position_label = QLabel("进度：0%")
        self.status_bar.addWidget(self.position_label)
        self.setStatusBar(self.status_bar)
        
        # 启用键盘快捷键
        self.text_edit.keyPressEvent = self.keyboard_pagination
        
        # 自动滚屏定时器
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.do_auto_scroll)'''
content = content.replace(old_init_ui, new_init_ui)
# ===== 4. 修改 show_ncx_toc 方法，适应浮动窗口 =====
old_show_ncx = '''    def show_ncx_toc(self, titles):
        """显示从 NCX 提取的目录"""
        self.toc_list.clear()
        self.chapter_positions = []
        for title in titles:
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, title)
            self.toc_list.addItem(item)
        if titles:
            self.toc_list.show()
            self.toc_label.show()
        else:
            self.toc_list.hide()
            self.toc_label.hide()'''
new_show_ncx = '''    def show_ncx_toc(self, titles):
        """显示从 NCX 提取的目录"""
        self.toc_list.clear()
        self.chapter_positions = []
        for title in titles:
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, title)
            self.toc_list.addItem(item)
        if titles:
            self.toc_list.show()
            self.toc_label.show()
            # 调整浮动窗口大小以适应目录
            self.bookshelf_dock.setMinimumWidth(250)
        else:
            self.toc_list.hide()
            self.toc_label.hide()'''
content = content.replace(old_show_ncx, new_show_ncx)
# ===== 5. 修改 build_table_of_contents 中的显示逻辑 =====
old_toc_show = '''            self.toc_list.show()
            self.toc_label.show()
            self.toc_list.setMinimumWidth(200)
        else:
            self.toc_list.hide()
            self.toc_label.hide()'''
new_toc_show = '''            self.toc_list.show()
            self.toc_label.show()
            # 调整浮动窗口大小
            self.bookshelf_dock.setMinimumWidth(250)
        else:
            self.toc_list.hide()
            self.toc_label.hide()'''
content = content.replace(old_toc_show, new_toc_show)
# ===== 6. 在菜单中添加"显示/隐藏书架"选项 =====
# 修改 create_menu_bar，在视图菜单中添加书架开关
old_view_menu = '''        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 主题子菜单
        theme_menu = QMenu("主题模式", self)'''
new_view_menu = '''        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 显示/隐藏书架
        toggle_bookshelf_action = QAction("显示书架", self)
        toggle_bookshelf_action.setCheckable(True)
        toggle_bookshelf_action.setChecked(True)
        toggle_bookshelf_action.triggered.connect(self.toggle_bookshelf)
        toggle_bookshelf_action.setShortcut("Ctrl+B")
        view_menu.addAction(toggle_bookshelf_action)
        
        view_menu.addSeparator()
        
        # 主题子菜单
        theme_menu = QMenu("主题模式", self)'''
if old_view_menu in content:
    content = content.replace(old_view_menu, new_view_menu)
else:
    print("⚠️ 未找到 view_menu，尝试其他方式...")
# ===== 7. 添加 toggle_bookshelf 方法 =====
toggle_method = '''    def toggle_bookshelf(self, checked):
        """显示/隐藏书架浮动窗口"""
        self.bookshelf_dock.setVisible(checked)
    
    def show_ncx_toc(self, titles):'''
content = content.replace('    def show_ncx_toc(self, titles):', toggle_method)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 浮动书架窗口改造完成！")
print("改进内容：")
print("1. 书架和目录改为 QDockWidget 浮动窗口")
print("2. 可自由拖动、调整大小、关闭")
print("3. 视图菜单增加'显示书架'开关（快捷键 Ctrl+B）")
print("4. 默认停靠在左侧，可拖出成为独立窗口")