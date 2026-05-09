import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QMenu,
    QToolBar, QStatusBar, QAction, QFileDialog, QMessageBox, QColorDialog,
    QSpinBox, QDoubleSpinBox, QLabel, QGroupBox, QCheckBox, QRadioButton,
    QScrollArea, QSplitter, QInputDialog, QListWidget, QListWidgetItem,
    QDialog, QDialogButtonBox, QDockWidget
)
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPalette, QIcon
from PyQt5.QtCore import Qt, QSettings, QTimer, QSize, QPropertyAnimation, QEasingCurve
# 主窗口类

# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class NovelReaderMainWindow(QMainWindow):
    def keyboard_pagination(self, event):
        """键盘翻页：方向键、PageUp/PageDown、空格键"""
        key = event.key()
        if key == Qt.Key_Up:
            # 向上翻页（滚动一行）
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            # 向上滚动一行
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.singleStep())
            event.accept()
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() - 10
            )
        elif key == Qt.Key_Down:
            # 向下翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() + 10
            )
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            event.accept()
        elif key == Qt.Key_PageUp:
            # 向上翻一页
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.pageStep())
            event.accept()
        elif key == Qt.Key_PageDown:
            # 向下翻一页
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() + vbar.pageStep())
            event.accept()
        elif key == Qt.Key_Space:
            # 空格触发自动滚屏开关
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            else:
                self.start_auto_scroll()
            event.accept()
    def prev_page(self):
        """上一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = max(0, current - page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    
    def next_page(self):
        """下一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = min(scrollbar.maximum(), current + page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    def wheel_event(self, event):
        """鼠标滚轮翻页"""
        # 获取滚轮滚动量
        delta = event.angleDelta().y()
        scrollbar = self.text_edit.verticalScrollBar()
        if delta > 0:
            # 向上滚动（上一行）
            scrollbar.setValue(scrollbar.value() - 20)
        else:
            # 向下滚动（下一行）
            scrollbar.setValue(scrollbar.value() + 20)
        event.accept()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("NovelReader", "LocalNovelReader")
        self.current_book_path = None
        self.reading_position = 0
        self.auto_scroll_enabled = False
        self.auto_scroll_speed = 5
        self.current_theme = "day"  # day, night, eye_care
        self.toc_list = QListWidget()
        self.toc_label = QLabel("目录")
        self.chapter_positions = []
        
        # 初始化UI
        self.init_ui()
        self.load_settings()
        self.restore_state()
        self.apply_theme()
        
        # 书签列表
        self.bookmark_list = []

    def load_settings(self):
        """加载设置"""
        self.settings = QSettings('NovelReader', 'Settings')
        self.font_size = self.settings.value('font_size', 18, int)
        self.line_spacing = self.settings.value('line_spacing', 1.5, float)
        self.font_family = self.settings.value('font_family', None, str)
        self.font_weight = self.settings.value('font_weight', None, int)
        self.theme = self.settings.value('theme', 'light', str)
        self.auto_scroll_speed = self.settings.value('auto_scroll_speed', 30, int)

    def toggle_bookshelf(self, checked):
        """显示/隐藏书架浮动窗口"""
        self.bookshelf_dock.setVisible(checked)
    
    def show_ncx_toc(self, titles):
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
            self.toc_label.hide()

    def keyboard_pagination(self, event):
        """键盘翻页：方向键、PageUp/PageDown、空格键"""
        key = event.key()
        if key == Qt.Key_Up:
            # 向上翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() - 10
            )
        elif key == Qt.Key_Down:
            # 向下翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() + 10
            )
        elif key == Qt.Key_Left:
            # 向左翻页（上一页）
            self.prev_page()
        elif key == Qt.Key_Right:
            # 向右翻页（下一页）
            self.next_page()
        elif key == Qt.Key_PageUp:
            # PageUp：向上翻一页
            self.prev_page()
        elif key == Qt.Key_PageDown:
            # PageDown：向下翻一页
            self.next_page()
        elif key == Qt.Key_Space:
            # 空格键：下一页
            self.next_page()
        else:
            # 其他按键交给默认处理
            super().keyPressEvent(event)
    
    def prev_page(self):
        """上一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = max(0, current - page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    
    def next_page(self):
        """下一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = min(scrollbar.maximum(), current + page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    def wheel_event(self, event):
        """键盘翻页：方向键、PageUp/PageDown、空格键"""
        key = event.key()
        if key == Qt.Key_Up:
            # 向上翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() - 10
            )
        elif key == Qt.Key_Down:
            # 向下翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() + 10
            )
        elif key == Qt.Key_Left:
            # 向左翻页（上一页）
            self.prev_page()
        elif key == Qt.Key_Right:
            # 向右翻页（下一页）
            self.next_page()
        elif key == Qt.Key_PageUp:
            # PageUp：向上翻一页
            self.prev_page()
        elif key == Qt.Key_PageDown:
            # PageDown：向下翻一页
            self.next_page()
        elif key == Qt.Key_Space:
            # 空格键：下一页
            self.next_page()
        else:
            # 其他按键交给默认处理
            super().keyPressEvent(event)
    
    def prev_page(self):
        """上一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = max(0, current - page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    
    def next_page(self):
        """下一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = min(scrollbar.maximum(), current + page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(400)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.page_anim.start()
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("喜阅")
        # 设置卡通书本图标
        # 强制设置窗口图标（移除 exists 检查，确保一定执行）
        try:
            from PyQt5.QtGui import QIcon
            icon_full_path = resource_path('book_icon.ico')
            self.setWindowIcon(QIcon(icon_full_path))
            print(f"✅ 窗口图标已设置：{icon_full_path}")
        except Exception as e:
            print(f"⚠️ 设置窗口图标失败：{e}")
        # self.setMinimumSize(400, 300) # 已注释，允许随意调整大小
        
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
        self.toc_label.setStyleSheet("font-weight: bold; color: #2E7D32; background-color: #A5D6A7; padding: 6px; border-radius: 3px; border: none;")
        bookshelf_layout.addWidget(self.toc_label)
        
        # 目录列表
        self.toc_list = QListWidget()
        self.toc_list.setVisible(False)
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        bookshelf_layout.addWidget(self.toc_list)


        # 书签标签
        self.bm_label = QLabel("书签")
        self.bm_label.setStyleSheet("font-weight: bold; color: #2E7D32; background-color: #A5D6A7; padding: 6px; border-radius: 3px; border: none;")
        bookshelf_layout.addWidget(self.bm_label)

        # 书签列表
        self.bm_list_widget = QListWidget()
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        self.bm_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bm_list_widget.customContextMenuRequested.connect(self.show_bookmark_context_menu)
        bookshelf_layout.addWidget(self.bm_list_widget)
        self.bookshelf_dock.setWidget(bookshelf_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.bookshelf_dock)
        # 设置书架蓝色调样式，无黑边
        self.bookshelf_dock.setStyleSheet("""
            QDockWidget {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F0F4F8, stop:1 #E1EBF5);
            }
            QDockWidget::title {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90CAF9, stop:1 #64B5F6);
                padding: 6px;
                color: white;
                font-weight: bold;
                border: none;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                border: none;
                background: #E3F2FD;
                border-radius: 3px;
            }
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                background: #BBDEFB;
            }
        """)
        
        # 设置主窗口分割线样式
        self.setStyleSheet("""
            QMainWindow::separator {
                width: 5px;
                background: #BBDEFB;
                border-radius: 2px;
            }
            QMainWindow::separator:hover {
                background: #64B5F6;
            }
        """)

        
        # ===== 创建中央阅读区域 =====
        self.reading_panel = QWidget()
        reading_layout = QVBoxLayout(self.reading_panel)
        reading_layout.setContentsMargins(0, 0, 0, 0)
        
        # 阅读文本区域
        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)  # 自动换行适应边框宽度
        self.text_edit.setWordWrapMode(True)  # 单词自动换行
        # 设置正文区域样式（清爽无框）
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: #FAFAFA;
                padding: 15px;
                font-size: 18px;
            }
        """)
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
        
        # 注册关闭事件处理
        self.closeEvent = self.on_close
        
        # 自动滚屏定时器
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.do_auto_scroll)
        
        # 添加右键菜单
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_text_context_menu)
        

        # 设置主窗口阴影效果（应用到内部容器，保留系统原生边框拖拽功能）
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        # 创建一个主容器包裹阅读面板
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 留出阴影空间
        main_layout.addWidget(self.reading_panel)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(33, 150, 243, 40))  # 淡蓝色阴影
        main_container.setGraphicsEffect(shadow)
        
        # 将容器设为中央部件
        self.setCentralWidget(main_container)
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        open_file_action = QAction("打开文件", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_file_action)
        
        open_folder_action = QAction("批量导入文件夹", self)
        open_folder_action.triggered.connect(self.import_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
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
        theme_menu = QMenu("主题模式", self)
        
        day_action = QAction("白天模式", self)
        day_action.triggered.connect(lambda: self.change_theme("day"))
        theme_menu.addAction(day_action)
        
        night_action = QAction("夜间模式", self)
        night_action.triggered.connect(lambda: self.change_theme("night"))
        theme_menu.addAction(night_action)
        
        eyecare_action = QAction("护眼模式", self)
        eyecare_action.triggered.connect(lambda: self.change_theme("eye_care"))
        theme_menu.addAction(eyecare_action)
        
        view_menu.addMenu(theme_menu)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction("全屏阅读", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        focus_action = QAction("专注模式", self)
        focus_action.triggered.connect(self.toggle_focus_mode)
        view_menu.addAction(focus_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu("设置")
        
        font_action = QAction("字体设置", self)
        font_action.triggered.connect(self.open_font_settings)
        settings_menu.addAction(font_action)
        
        background_action = QAction("自定义背景色", self)
        background_action.triggered.connect(self.custom_background_color)
        settings_menu.addAction(background_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        
        search_action = QAction("全文搜索", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.search_text)
        tools_menu.addAction(search_action)
        
        clean_text_action = QAction("文本优化清理", self)
        clean_text_action.triggered.connect(self.clean_current_text)
        tools_menu.addAction(clean_text_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def create_tool_bar(self):
        """创建工具栏 - 马卡龙风格"""
        toolbar = self.addToolBar("主工具栏")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(22, 22)) # 缩小一点更紧凑
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 文字在图标下方
        
        # 马卡龙配色样式表 (CSS)
        macaron_css = """
                        QToolBar {
                spacing: 3px;
                padding: 5px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border: none;
            }
            QToolButton {
                border: none;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #E3F2FD);
                padding: 4px 8px;
                margin: 2px;
                min-width: 40px;
                color: #1565C0;
                font-weight: bold;
            }
            QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BBDEFB, stop:1 #90CAF9);
            }
            QToolButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90CAF9, stop:1 #64B5F6);
                padding: 5px 7px 3px 9px;
            }

            QToolButton {
                background-color: #FFFFFF;
                border: 2px solid #AEC6CF; /* 马卡龙蓝边框 */
                border-radius: 12px;
                padding: 4px 2px;
                color: #555555;
                font-size: 14px; /* 字体加大 */
                font-weight: bold;
                font-family: "Microsoft YaHei";
            }
            QToolButton:hover {
                background-color: #FDFD96; /* 马卡龙黄悬停 */
                border-color: #FFB7B2;
            }
            QToolButton:pressed {
                background-color: #77DD77; /* 马卡龙绿按下 */
                border-color: #C3B1E1;
            }
            QToolButton:checked {
                background-color: #FFB7B2; /* 选中状态 (马卡龙粉) */
                color: white;
                border-color: #FF6961;
            }
        """
        toolbar.setStyleSheet(macaron_css)
        
        # 添加功能按钮
        # 主题切换
        toolbar.addAction("☀️ 白天", lambda: self.change_theme("day"))
        toolbar.addAction("🌙 夜间", lambda: self.change_theme("night"))
        toolbar.addAction("🌿 护眼", lambda: self.change_theme("eye_care"))
        
        toolbar.addSeparator()
        
        # 翻页控制
        prev_action = QAction("⬅️ 上页", self)
        prev_action.triggered.connect(self.prev_page)
        toolbar.addAction(prev_action)
        
        next_action = QAction("➡️ 下页", self)
        next_action.triggered.connect(self.next_page)
        toolbar.addAction(next_action)
        
        toolbar.addSeparator()
        
        # 自动滚屏
        self.auto_scroll_action = QAction("📜 滚屏", self)
        self.auto_scroll_action.setCheckable(True)
        self.auto_scroll_action.setShortcut("Ctrl+Space")
        self.auto_scroll_action.triggered.connect(self.toggle_auto_scroll)
        toolbar.addAction(self.auto_scroll_action)
        
        # 滚屏速度调节
        speed_down_action = QAction("🐢 减速", self)
        speed_down_action.triggered.connect(lambda: self.adjust_scroll_speed(-5))
        toolbar.addAction(speed_down_action)
        
        speed_up_action = QAction("🐇 加速", self)
        speed_up_action.triggered.connect(lambda: self.adjust_scroll_speed(5))
        toolbar.addAction(speed_up_action)
        
        # 专注模式
        focus_action = QAction("🧘 专注", self)
        
        toolbar.addSeparator()
        
        # 书签功能
        add_bm_action = QAction("🔖 加签", self)
        add_bm_action.setShortcut("Ctrl+D")
        add_bm_action.triggered.connect(self.add_bookmark)
        toolbar.addAction(add_bm_action)
        
        list_bm_action = QAction("📋 书签", self)
        list_bm_action.triggered.connect(self.show_bookmark_list)
        toolbar.addAction(list_bm_action)
        focus_action.triggered.connect(self.toggle_focus_mode)
        toolbar.addAction(focus_action)
        self.toolbar = toolbar
        self.base_icon_size = 22

    def open_file_dialog(self):
        """打开文件对话框"""
        file_filters = "小说文件 (*.txt *.epub *.mobi *.pdf);;所有文件 (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "打开小说文件", "", file_filters)
        if file_path:
            self.load_book(file_path)
            
    def load_book(self, file_path):
        """加载书籍文件"""
        try:
            self.current_book_path = file_path
            self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")
            
            # 判断是否为 PDF 文件，使用图片分页模式打开
            if file_path.lower().endswith('.pdf'):
                self.load_pdf_as_images(file_path)
                return
                
            from file_handler import FileHandler
            handler = FileHandler()
            
            content = handler.read_file(file_path)
            
            # 智能识别内容类型：如果是HTML则使用富文本显示，支持图片
            is_html = False
            stripped = content.strip()
            if stripped.startswith('<html') or stripped.startswith('<!DOCTYPE') or '<img' in stripped:
                is_html = True
            
            if is_html:
                self.text_edit.setHtml(content)
            else:
                self.text_edit.setPlainText(content)
            self.current_book_path = file_path
            self.load_bookmarks()
            self.load_bookmarks()
            self.refresh_bookmark_list() # 加载书签
            self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")
            
            # 解析目录并生成目录面板
            # 优先使用 NCX 目录（如果有）
            ncx_toc = getattr(handler, 'ncx_toc', [])
            if ncx_toc:
                self.show_ncx_toc(ncx_toc)
            else:
                self.build_table_of_contents(content, is_html)
            # 确保目录显示在书架面板
            self.toc_label.show()
            self.toc_list.show()
            
            # 恢复上次阅读位置
            position = self.settings.value(f"position_{file_path}", 0, int)
            if position > 0 and position < len(content):
                cursor = self.text_edit.textCursor()
                cursor.setPosition(position)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                
            # 去掉弹窗，直接加载
        except Exception as e:
            # 双层保护，绝对不闪退
            error_msg = f"加载文件失败：{str(e)}\n\n请检查文件是否存在、损坏或格式不支持。"
            try:
                QMessageBox.critical(self, "错误", error_msg)
            except:
                # 如果连弹窗都失败了，至少保证不崩溃
                print(error_msg)
    
            
    def load_pdf_as_images(self, file_path):
        """将 PDF 渲染为图片并分页显示，保留原格式"""
        try:
            import fitz # PyMuPDF
            from PyQt5.QtGui import QImage, QPixmap
            from PyQt5.QtCore import Qt
            
            self.text_edit.clear()
            self.text_edit.setReadOnly(True) # PDF 模式下设为只读
            
            doc = fitz.open(file_path)
            cursor = self.text_edit.textCursor()
            
            # 设置缩放比例，2.0 比较清晰
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=mat)
                
                # 转换为 QImage
                img_data = pix.tobytes("png")
                qimage = QImage.fromData(img_data)
                
                if qimage.isNull():
                    continue
                    
                pixmap = QPixmap.fromImage(qimage)
                
                # 插入图片
                cursor.insertImage(pixmap.toImage())
                cursor.insertText("\n") # 分页间隔
                
            doc.close()
            self.status_bar.showMessage(f"✅ PDF 加载完成，共 {len(doc)} 页", 3000)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载 PDF 失败：{str(e)}")

    def build_table_of_contents(self, content, is_html):
        """解析文本内容，生成目录列表"""
        import re
        
        self.toc_list.clear()
        self.chapter_positions = []
        
        if is_html:
            # HTML格式：多重策略识别章节标题
            import re
            from bs4 import BeautifulSoup
            
            # 策略1：优先匹配<h1>-<h6>标签
            h_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            for match in re.finditer(h_pattern, content, re.IGNORECASE):
                title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                # 过滤太短或包含广告词的标题
                if title and len(title) > 2 and not any(kw in title for kw in ['Copyright', '版权', 'www.', 'http']):
                    self.chapter_positions.append((title, match.start()))
            
            # 策略2：如果<h1>-<h6>没找到，尝试匹配常见章节class/id
            if not self.chapter_positions:
                soup = BeautifulSoup(content, 'html.parser')
                chapter_patterns = [
                    {'name': True, 'class': lambda c: c and any('chapter' in str(x).lower() or 'title' in str(x).lower() for x in c)},
                    {'name': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']},
                    {'name': 'p', 'class': lambda c: c and any('title' in str(x).lower() or 'chapter' in str(x).lower() for x in c)},
                    {'name': 'div', 'class': lambda c: c and any('chapter' in str(x).lower() or 'title' in str(x).lower() for x in c)},
                ]
                
                for tag in soup.find_all(lambda tag: any(
                    (pattern.get('name') is None or pattern.get('name') == True or tag.name == pattern['name']) and
                    (pattern.get('class') is None or (tag.get('class') and pattern['class'](tag.get('class'))))
                    for pattern in chapter_patterns
                )):
                    title = tag.get_text(strip=True)
                    # 检查是否像章节标题
                    if title and len(title) > 2 and len(title) < 100:
                        if re.match(r'^\s*(第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]|Chapter\s+[0-9IVXLCDM]+|Part\s+[0-9IVXLCDM]+)', title, re.IGNORECASE):
                            # 找到在原始content中的位置
                            pos = content.find(title)
                            if pos != -1:
                                self.chapter_positions.append((title, pos))
                                if len(self.chapter_positions) >= 5:  # 找到几个就够了
                                    break
            
            # 策略3：如果还是没找到，尝试从文本内容中查找（兼容纯文本风格的HTML）
            if not self.chapter_positions:
                text_content = BeautifulSoup(content, 'html.parser').get_text('\n')
                lines = text_content.split('\n')
                chapter_patterns_text = [
                    r'^\s*第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]\s*.*$',
                    r'^\s*Chapter\s+[0-9IVXLCDM]+[.:、\s].*$',
                    r'^\s*Part\s+[0-9IVXLCDM]+[.:、\s].*$',
                ]
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if not stripped or len(stripped) > 100:
                        continue
                    for pat in chapter_patterns_text:
                        if re.match(pat, stripped, re.IGNORECASE):
                            pos = text_content[:i].count('\n')  # 估算位置
                            self.chapter_positions.append((stripped, pos))
                            break
        else:
            # 纯文本格式：匹配常见章节标题
            # 支持格式：第X章、第X节、第X卷、Chapter X、Ch.X、数字序号章节等
            patterns = [
                r'^\s*第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集]\s*.*$',  # 第一章、第二节、第三卷
                r'^\s*[\[【（(]?第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集][\]】）)]?\s*.*$',  # 【第一章】等
                r'^\s*(?:Chapter|Ch|Section|Part|Volume)\s*[0-9IVXLCDM]+[.:、\s].*$',  # Chapter 1、Part I
                r'^\s*[\[【（(]?[0-9]+[、.．\s}])].*$',  # 1.、1、1)
                r'^\s*[\[【（(]?[0-9]+[\]】）)]\s*.*$',  # [1]、【1】
                r'^\s*[\[【（(]?[零一二三四五六七八九十百千万]+[、.．\s}])].*$',  # 一、一.
            ]
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped:
                    continue
                for pat in patterns:
                    if re.match(pat, stripped, re.IGNORECASE):
                        # 计算这个章节在全文中的字符位置（更精确）
                        char_pos = sum(len(l) + 1 for l in lines[:i])
                        self.chapter_positions.append((stripped, char_pos))
                        break
        
        # 填充目录列表（存储标题文本，跳转时用文档查找）
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, title)  # 存储标题文本用于查找
                self.toc_list.addItem(item)
            self.toc_list.show()
            self.toc_label.show()
            # 调整浮动窗口大小
            self.bookshelf_dock.setMinimumWidth(250)
        else:
            self.toc_list.hide()
            self.toc_label.hide()
    
    def jump_to_chapter(self, item):
        """点击目录项，跳转到对应章节位置"""
        title = item.text()
        # 用 QTextDocument.find 查找章节标题文本
        # 从文档开头开始查找
        cursor = QTextCursor(self.text_edit.document())
        cursor.movePosition(QTextCursor.Start)
        self.text_edit.setTextCursor(cursor)
        # 查找章节标题
        found = self.text_edit.find(title)
        if found:
            self.text_edit.ensureCursorVisible()
            self.text_edit.setFocus()
        else:
            # 如果精确查找失败，尝试只查找章节标题的前几个字（去掉序号）
            import re
            # 匹配 "第X章" 或 "第X节" 等
            match = re.match(r'^\s*([\[【（(]?第[^\]】）)]+[\]】）)]?\s*)', title)
            if match:
                prefix = match.group(1)
                cursor2 = QTextCursor(self.text_edit.document())
                cursor2.movePosition(QTextCursor.Start)
                self.text_edit.setTextCursor(cursor2)
                if self.text_edit.find(prefix):
                    self.text_edit.ensureCursorVisible()
                    self.text_edit.setFocus()

    def import_folder(self):
        """批量导入文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if folder_path:
            # 初始化 bookshelf_data
            if not hasattr(self, 'bookshelf_data'):
                self.bookshelf_data = {}
            
            # 添加到书架
            category_name = os.path.basename(folder_path)
            category_item = QTreeWidgetItem(self.books_tree, [category_name])
            category_item.setData(0, Qt.UserRole, "__category__")
            
            # 存储这个分类下的所有书籍
            books_in_category = []
            
            # 遍历文件夹中的小说文件，支持多层文件夹嵌套
            extensions = ['.txt', '.epub', '.mobi', '.pdf']
            total_files = 0
            for root, dirs, files in os.walk(folder_path):
                # 为子文件夹创建分类节点
                if root != folder_path:
                    rel_path = os.path.relpath(root, folder_path)
                    sub_category = QTreeWidgetItem(category_item, [rel_path])
                    sub_category.setData(0, Qt.UserRole, "__subcategory__")
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(sub_category, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            books_in_category.append({'name': file, 'path': full_path})
                            total_files += 1
                else:
                    # 根文件夹下的文件直接添加到主分类下
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in extensions:
                            full_path = os.path.join(root, file)
                            book_item = QTreeWidgetItem(category_item, [file])
                            book_item.setData(0, Qt.UserRole, full_path)
                            books_in_category.append({'name': file, 'path': full_path})
                            total_files += 1
            
            # 保存到 bookshelf_data
            self.bookshelf_data[category_name] = books_in_category
            
            # 去掉导入确认弹窗，直接导入
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")
    def import_single_book_to_bookshelf(self, category_item=None):
        """导入单本书到书架，可指定分类节点"""
        file_filters = "小说文件 (*.txt *.epub *.mobi *.pdf);;所有文件 (*.*)"
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择要导入的小说文件", "", file_filters)
        if not file_paths:
            return
        # 初始化 bookshelf_data
        if not hasattr(self, 'bookshelf_data'):
            self.bookshelf_data = {}
        if category_item is None:
            # 未指定分类，使用文件名作为分类名
            cat_name = "导入书籍"
            category_item = QTreeWidgetItem(self.books_tree, [cat_name])
            category_item.setData(0, Qt.UserRole, "__category__")
            if cat_name not in self.bookshelf_data:
                self.bookshelf_data[cat_name] = []
            books_in_category = self.bookshelf_data[cat_name]
        else:
            cat_name = category_item.text(0)
            if cat_name not in self.bookshelf_data:
                self.bookshelf_data[cat_name] = []
            books_in_category = self.bookshelf_data[cat_name]
        count = 0
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            book_item = QTreeWidgetItem(category_item, [file_name])
            book_item.setData(0, Qt.UserRole, file_path)
            books_in_category.append({'name': file_name, 'path': file_path})
            count += 1
        print(f"✅ 已导入 {count} 本书到分类「{cat_name}」")
    def import_folder_to_category(self, category_item):
        """导入文件夹到指定分类"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择要导入的文件夹")
        if not folder_path:
            return
        cat_name = category_item.text(0)
        if not hasattr(self, 'bookshelf_data'):
            self.bookshelf_data = {}
        if cat_name not in self.bookshelf_data:
            self.bookshelf_data[cat_name] = []
        books_in_category = self.bookshelf_data[cat_name]
        extensions = ['.txt', '.epub', '.mobi', '.pdf']
        total_files = 0
        for root, dirs, files in os.walk(folder_path):
            if root != folder_path:
                rel_path = os.path.relpath(root, folder_path)
                sub_category = QTreeWidgetItem(category_item, [rel_path])
                sub_category.setData(0, Qt.UserRole, "__subcategory__")
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        full_path = os.path.join(root, file)
                        book_item = QTreeWidgetItem(sub_category, [file])
                        book_item.setData(0, Qt.UserRole, full_path)
                        books_in_category.append({'name': file, 'path': full_path})
                        total_files += 1
            else:
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        full_path = os.path.join(root, file)
                        book_item = QTreeWidgetItem(category_item, [file])
                        book_item.setData(0, Qt.UserRole, full_path)
                        books_in_category.append({'name': file, 'path': full_path})
                        total_files += 1
        print(f"✅ 已导入 {total_files} 本书到分类「{cat_name}」")
    def open_book_from_tree(self, item, column):
        """从书架树打开书籍"""
        file_path = item.data(0, Qt.UserRole)
        if not file_path or str(file_path).startswith("__"):
            return
        # 保护：跳过分类节点和无效文件
        if not file_path or file_path.startswith("__"):
            return
        if os.path.exists(file_path):
            self.load_book(file_path)
            # 展开书架树中该书的父节点，方便查看
            parent = item.parent()
            if parent:
                parent.setExpanded(True)
            
    def show_bookshelf_context_menu(self, position):
        """显示书架右键菜单"""
        item = self.books_tree.itemAt(position)
        menu = QMenu()
        
        if item is None:
            # 空白处右键：新建分类 + 导入书籍
            add_category_action = menu.addAction("📁 新建分类")
            import_file_action = menu.addAction("📂 导入书籍文件")
            import_folder_action = menu.addAction("📚 导入书籍文件夹")
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if action == add_category_action:
                name, ok = QInputDialog.getText(self, "新建分类", "请输入分类名称：")
                if ok and name:
                    QTreeWidgetItem(self.books_tree, [name])
            elif action == import_file_action:
                self.import_single_book_to_bookshelf()
            elif action == import_folder_action:
                self.import_folder()
        else:
            # 选中了项目
            is_category = (item.parent() is None)
            if is_category:
                delete_cat_action = menu.addAction("🗑️ 删除分类")
                import_file_action = menu.addAction("📂 导入书籍到本分类")
                import_folder_action = menu.addAction("📚 导入文件夹到本分类")
            else:
                delete_book_action = menu.addAction("🗑️ 删除本书")
                
            action = menu.exec_(self.books_tree.mapToGlobal(position))
            if is_category:
                if action == delete_cat_action:
                    self.delete_selected_category()
                elif action == import_file_action:
                    self.import_single_book_to_bookshelf(item)
                elif action == import_folder_action:
                    self.import_folder_to_category(item)
            elif not is_category and action == delete_book_action:
                self.delete_selected_book()
                

    def delete_selected_book(self):
        """删除书架中选中的书籍"""
        from PyQt5.QtWidgets import QMessageBox
        item = self.books_tree.currentItem()
        if not item or not item.data(0, Qt.UserRole):
            self.status_bar.showMessage("⚠️ 请先选择一本书", 3000)
            return
        book_path = item.data(0, Qt.UserRole)
        book_name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要从书架中删除「{book_name}」吗？\n（不会删除源文件）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 从书架树中移除
            parent = item.parent()
            if parent:
                parent.removeChild(item)
            else:
                root = self.books_tree.invisibleRootItem()
                root.removeChild(item)
            self.status_bar.showMessage(f"🗑️ 已从书架移除：{book_name}", 3000)

    def delete_selected_category(self):
        """删除书架中选中的分类"""
        item = self.books_tree.currentItem()
        if not item or item.parent() is not None:
            return
        cat_name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除分类「{cat_name}」吗？\n（该分类下的书籍也会从书架移除，不会删除源文件）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            root = self.books_tree.invisibleRootItem()
            root.removeChild(item)
            # 同步更新 bookshelf_data
            if hasattr(self, "bookshelf_data") and cat_name in self.bookshelf_data:
                del self.bookshelf_data[cat_name]
            self.status_bar.showMessage(f"🗑️ 已删除分类：{cat_name}", 3000)

    def change_theme(self, theme):
        """切换主题"""
        self.current_theme = theme
        self.apply_theme()
        
    def apply_theme(self):
        """应用主题配色"""
        if self.current_theme == "day":
            bg_color = "#FFFFFF"  # 纯白
            text_color = "#000000"  # 纯黑
            link_color = "#0000EE"
        elif self.current_theme == "night":
            bg_color = "#1A1A1A"  # 深黑
            text_color = "#CCCCCC"  # 浅灰
            link_color = "#8888FF"
        elif self.current_theme == "eye_care":
            bg_color = "#CCE8CF"  # 豆沙绿
            text_color = "#000000"  # 纯黑
            link_color = "#006600"
        else:
            bg_color = "#FFFFFF"
            text_color = "#000000"
            link_color = "#0000EE"
            
        # 使用 setStyleSheet 确保优先级最高，直接覆盖阅读区背景
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                color: {text_color};
                selection-background-color: #ADD8E6;
                selection-color: #000000;
                border: none;
            }}
        """)
        self.status_bar.showMessage(f"已切换至{'白天' if self.current_theme=='day' else '夜间' if self.current_theme=='night' else '护眼'}模式", 2000)
        
    def toggle_fullscreen(self):
        """切换全屏"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def toggle_focus_mode(self):
        """切换专注模式（隐藏/显示书架浮动窗口）"""
        if self.bookshelf_dock.isVisible():
            self.bookshelf_dock.hide()
        else:
            self.bookshelf_dock.show()
            
    def toggle_auto_scroll(self, checked):
        """切换自动滚屏"""
        if checked:
            self.auto_scroll_enabled = True
            # 速度值越大，间隔越小，滚动越快
            interval = max(10, 100 - self.auto_scroll_speed * 8)
            self.auto_scroll_timer.start(int(interval))
            self.auto_scroll_action.setText("⏸️ 暂停")
            self.status_bar.showMessage(f"📜 滚屏已开启（速度：{self.auto_scroll_speed}），点击暂停或按 Ctrl+Space 停止", 5000)
        else:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()
            self.auto_scroll_action.setText("📜 滚屏")
            self.status_bar.showMessage("📜 滚屏已暂停", 3000)
            

    def adjust_scroll_speed(self, delta):
        """调整滚屏速度"""
        self.auto_scroll_speed = max(5, min(95, self.auto_scroll_speed + delta))
        self.settings.setValue('auto_scroll_speed', self.auto_scroll_speed)
        # 如果正在滚屏，动态调整速度
        if self.auto_scroll_enabled:
            interval = max(10, 100 - self.auto_scroll_speed * 8)
            self.auto_scroll_timer.setInterval(int(interval))
        direction = "⬆️ 加速" if delta > 0 else "⬇️ 减速"
        self.status_bar.showMessage(f"{direction} 当前滚屏速度：{self.auto_scroll_speed}", 3000)

    def do_auto_scroll(self):
        """执行自动滚屏"""
        scroll_bar = self.text_edit.verticalScrollBar()
        current_value = scroll_bar.value()
        # 根据速度调节每次滚动像素数，实现平滑滚屏效果
        step = max(1, int(self.auto_scroll_speed / 10))
        scroll_bar.setValue(current_value + step)
        # 滚到底部时自动停止
        if current_value >= scroll_bar.maximum() - 10:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()
            self.auto_scroll_action.setChecked(False)
            self.status_bar.showMessage("📜 已滚到底部，滚屏结束", 3000)
        
    def update_position(self):
        """更新阅读进度"""
        cursor = self.text_edit.textCursor()
        total_blocks = self.text_edit.document().blockCount()
        current_block = cursor.blockNumber()
        if total_blocks > 0:
            progress = int((current_block / total_blocks) * 100)
            self.position_label.setText(f"进度：{progress}%")
            
            # 保存当前位置
            if self.current_book_path:
                self.settings.setValue(f"position_{self.current_book_path}", cursor.position())
                
    def open_font_settings(self):
        """打开字体设置对话框"""
        from PyQt5.QtWidgets import QFontComboBox, QComboBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle("字体设置")
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        # 字体选择
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体:"))
        font_combo = QFontComboBox()
        current_font = self.text_edit.font()
        font_combo.setCurrentFont(current_font)
        font_layout.addWidget(font_combo)
        layout.addLayout(font_layout)

        # 字号设置
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("字号:"))
        size_spin = QSpinBox()
        size_spin.setValue(current_font.pointSize())
        size_spin.setRange(8, 48)
        size_layout.addWidget(size_spin)
        layout.addLayout(size_layout)

        # 行高设置
        line_height_layout = QHBoxLayout()
        line_height_layout.addWidget(QLabel("行高:"))
        line_height_spin = QDoubleSpinBox()
        current_line_height = self.text_edit.document().documentMargin()
        if current_line_height <= 0:
            current_line_height = 1.2
        line_height_spin.setValue(current_line_height / current_font.pointSize())
        line_height_spin.setRange(0.8, 3.0)
        line_height_spin.setSingleStep(0.1)
        line_height_layout.addWidget(line_height_spin)
        layout.addLayout(line_height_layout)

        # 字重（粗细）选择
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("粗细:"))
        weight_combo = QComboBox()
        from PyQt5.QtGui import QFont
        weight_combo.addItem("正常", QFont.Normal)
        weight_combo.addItem("粗体", QFont.Bold)
        # 匹配当前字重
        current_weight = current_font.weight()
        if current_weight >= QFont.Bold:
            weight_combo.setCurrentIndex(1)
        else:
            weight_combo.setCurrentIndex(0)
        weight_layout.addWidget(weight_combo)
        layout.addLayout(weight_layout)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # 应用设置
        def accept():
            from PyQt5.QtGui import QFont
            new_font = font_combo.currentFont()
            new_font.setPointSize(size_spin.value())
            new_font.setWeight(weight_combo.currentData())
            self.text_edit.setFont(new_font)
            # 设置行高
            self.text_edit.document().setDocumentMargin(line_height_spin.value() * new_font.pointSize())
            # 保存设置
            self.settings.setValue("font_family", new_font.family())
            self.settings.setValue("font_size", size_spin.value())
            self.settings.setValue("font_weight", new_font.weight())
            self.settings.setValue("line_spacing", line_height_spin.value())
            self.status_bar.showMessage(f"字体设置已更新：{new_font.family()} {new_font.pointSize()}pt", 3000)
            dialog.accept()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        # 应用设置
        dialog.exec_()

    def custom_background_color(self):
        """自定义背景颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.text_edit.palette()
            palette.setColor(QPalette.Base, color)
            self.text_edit.setPalette(palette)
            
    def search_text(self):
        """全文搜索"""
        text, ok = QInputDialog.getText(self, "全文搜索", "请输入要搜索的关键词：")
        if ok and text:
            document = self.text_edit.document()
            cursor = QTextCursor(document)
            count = 0
            while not cursor.isNull() and not cursor.atEnd():
                cursor = document.find(text, cursor)
                if not cursor.isNull():
                    # 高亮找到的文本
                    cursor.select(QTextCursor.WordUnderCursor)
                    count += 1
                    
            if count > 0:
                QMessageBox.information(self, "搜索完成", f"共找到 {count} 处匹配")
            else:
                QMessageBox.information(self, "搜索完成", "未找到匹配内容")
                
    def clean_current_text(self):
        """清理当前文本"""
        from text_processor import TextProcessor
        processor = TextProcessor()
        
        current_text = self.text_edit.toPlainText()
        cleaned = processor.clean_text(current_text)
        self.text_edit.setPlainText(cleaned)
        QMessageBox.information(self, "完成", "文本清理已完成")


    def show_text_context_menu(self, pos):
        """文本区域右键菜单"""
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        # 添加书签
        add_bm_action = menu.addAction("🔖 添加书签到当前位置")
        add_bm_action.triggered.connect(self.add_bookmark)
        # 打开书签管理
        list_bm_action = menu.addAction("🔄 刷新书签列表")
        list_bm_action.triggered.connect(self.show_bookmark_list)
        # 显示菜单
        menu.exec_(self.text_edit.mapToGlobal(pos))
    
    def get_position_preview(self, pos):
        """获取位置附近的文本预览"""
        try:
            if not hasattr(self, 'text_edit') or not self.text_edit:
                return "位置 " + str(pos)
            cursor = self.text_edit.textCursor()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            preview = cursor.selectedText().strip()
            if len(preview) > 50:
                preview = preview[:50]
            return preview if preview else "位置 " + str(pos)
        except Exception as e:
            print(f"⚠️ get_position_preview 错误：{e}")
            return "位置 " + str(pos)

    def add_bookmark(self):
        """添加书签（支持多条，带日期）"""
        try:
            from datetime import datetime
            if not hasattr(self, 'current_book_path') or not self.current_book_path:
                QMessageBox.warning(self, "警告", "请先打开一本书籍")
                return
            if not hasattr(self, 'text_edit') or not self.text_edit:
                QMessageBox.warning(self, "警告", "阅读器未初始化")
                return
            center_point = self.text_edit.viewport().rect().center()
            cursor = self.text_edit.cursorForPosition(center_point)
            pos = cursor.position()
            preview = self.get_position_preview(pos)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            if not hasattr(self, 'bookmark_list'):
                self.bookmark_list = []
            self.bookmark_list.append({'position': pos, 'preview': preview, 'time': timestamp})
            self.save_bookmarks()
            self.refresh_bookmark_list()
            if hasattr(self, 'status_bar') and self.status_bar:
                self.status_bar.showMessage(f"✅ 书签已添加：{timestamp}", 3000)
        except Exception as e:
            error_msg = f"添加书签失败：{str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(self, "错误", error_msg)

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

    def refresh_bookmark_list(self):
        """刷新书签列表（显示日期）"""
        if not hasattr(self, 'bm_list_widget'):
            return
        self.bm_list_widget.clear()
        if not hasattr(self, 'bookmark_list') or not self.bookmark_list:
            return
        # 按位置排序
        for i, bm in enumerate(sorted(self.bookmark_list, key=lambda x: x['position'])):
            item_text = f"[{bm['time']}] {bm['preview'][:30]}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, bm['position'])
            item.setData(Qt.UserRole + 1, i)  # 存储索引
            self.bm_list_widget.addItem(item)

    def jump_to_selected_bookmark(self, checked=None):
        """跳转到选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            return
        pos = item.data(Qt.UserRole)
        # 使用 setPosition 直接跳转（更准确更高效）
        cursor = self.text_edit.textCursor()
        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
    def delete_selected_bookmark(self):
        """删除选中的书签"""
        item = self.bm_list_widget.currentItem()
        if not item:
            self.status_bar.showMessage("⚠️ 请先选择一个书签", 3000)
            return
        
        idx = item.data(Qt.UserRole + 1)
        if idx is None or idx >= len(self.bookmark_list):
            return
            
        deleted_bm = self.bookmark_list.pop(idx)
        self.save_bookmarks()
        self.refresh_bookmark_list()
        self.status_bar.showMessage(f"🗑️ 已删除书签：{deleted_bm['time']} {deleted_bm['preview'][:20]}", 3000)


    def show_bookmark_context_menu(self, position):
        """显示书签右键菜单"""
        menu = QMenu()
        delete_action = menu.addAction("🗑️ 删除此书签")
        action = menu.exec_(self.bm_list_widget.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_bookmark()

    def on_close(self, event):
        """关闭窗口时自动保存所有状态"""
        print("💾 正在保存阅读状态...")
        # 保存当前打开的书籍路径
        if self.current_book_path:
            self.settings.setValue("last_opened_book", self.current_book_path)
        # 保存当前阅读进度
        cursor = self.text_edit.textCursor()
        if self.current_book_path:
            self.settings.setValue(f"position_{hash(self.current_book_path)}", cursor.position())
        # 保存字体设置
        font = self.text_edit.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())
        self.settings.setValue("font_weight", font.weight())
        line_height = self.text_edit.document().documentMargin() / font.pointSize() if font.pointSize() > 0 else 1.2
        self.settings.setValue("line_spacing", line_height)
        # 保存当前主题模式
        self.settings.setValue("current_theme", self.current_theme)
        # 保存窗口大小和位置
        self.settings.setValue("window_geometry", self.saveGeometry())
        self.settings.setValue("window_state", self.saveState())
        # 保存书架面板状态（是否浮动、位置等）
        self.settings.setValue("bookshelf_floating", self.bookshelf_dock.isFloating())
        self.settings.setValue("bookshelf_visible", self.bookshelf_dock.isVisible())
        # 保存所有书签（已经在添加/删除时实时保存，这里再确保一次）
        self.save_bookmarks()
        # 保存书架中所有导入的书籍
        if hasattr(self, 'bookshelf_data'):
            self.settings.setValue("bookshelf_data", self.bookshelf_data)
            # 保存展开/折叠状态
            expanded_states = []
            root = self.books_tree.invisibleRootItem()
            for i in range(root.childCount()):
                item = root.child(i)
                expanded_states.append(item.isExpanded())
            self.settings.setValue("bookshelf_expanded", expanded_states)
        print("✅ 所有状态已保存！")
        event.accept()
    
    def restore_state(self):
        """启动时恢复上次关闭时的状态"""
        # 恢复窗口大小和位置
        geometry = self.settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.settings.value("window_state")
        if state:
            self.restoreState(state)
        # 恢复书架面板状态
        floating = self.settings.value("bookshelf_floating", False)
        visible = self.settings.value("bookshelf_visible", True)
        if isinstance(floating, str):
            floating = floating == "true"
        if isinstance(visible, str):
            visible = visible == "true"
        self.bookshelf_dock.setFloating(floating)
        self.bookshelf_dock.setVisible(visible)
        # 恢复字体设置
        font_family = self.settings.value("font_family", "Microsoft YaHei")
        font_size = int(self.settings.value("font_size", 18))
        font_weight = int(self.settings.value("font_weight", 50))  # QFont.Normal
        line_spacing = float(self.settings.value("line_spacing", 1.2))
        from PyQt5.QtGui import QFont
        font = QFont(font_family, font_size)
        font.setWeight(font_weight)
        self.text_edit.setFont(font)
        self.text_edit.document().setDocumentMargin(line_spacing * font_size)
        # 恢复主题模式
        theme = self.settings.value("current_theme", "day")
        self.current_theme = theme
        # 恢复最后打开的书籍和阅读进度
        last_book = self.settings.value("last_opened_book")
        if last_book and os.path.exists(last_book):
            self.load_book(last_book)
            # 恢复阅读进度
            pos_key = f"position_{hash(last_book)}"
            last_pos = self.settings.value(pos_key, 0)
            if last_pos:
                cursor = self.text_edit.textCursor()
                cursor.setPosition(int(last_pos))
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                self.status_bar.showMessage(f"📖 已恢复到上次阅读进度", 3000)
        
        # 恢复书架中的所有书籍
        saved_books = self.settings.value("bookshelf_data")
        if saved_books and hasattr(self, 'books_tree'):
            # 清空现有树
            self.books_tree.clear()
            self.bookshelf_data = saved_books
            # 重建书架树
            for folder_name, book_list in self.bookshelf_data.items():
                folder_item = QTreeWidgetItem(self.books_tree, [folder_name])
                for book in book_list:
                    book_item = QTreeWidgetItem(folder_item, [book['name']])
                    book_item.setData(0, Qt.UserRole, book['path'])
            # 恢复展开/折叠状态
            expanded_states = self.settings.value("bookshelf_expanded")
            if expanded_states:
                root = self.books_tree.invisibleRootItem()
                for i in range(root.childCount()):
                    item = root.child(i)
                    if i < len(expanded_states):
                        item.setExpanded(bool(expanded_states[i]))
            print("✅ 书库已恢复")
        
        # 加载所有书籍的书签（遍历 bookshelf_data 中的所有书）
        if hasattr(self, 'bookshelf_data'):
            for category_name, books in self.bookshelf_data.items():
                for book in books:
                    book_path = book['path']
                    key = "bookmarks_" + hash(book_path).__str__()
                    bookmarks = self.settings.value(key, [])
                    if bookmarks:
                        print(f"  📑 已加载 {os.path.basename(book_path)} 的 {len(bookmarks)} 个书签")
        # 如果当前打开了书，加载它的书签
        if self.current_book_path:
            self.load_bookmarks()
            if hasattr(self, 'bookmark_list') and self.bookmark_list:
                print(f"✅ 已加载当前书籍的 {len(self.bookmark_list)} 个书签")



    
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

    def show_bookmark_list(self):
        """显示书签列表（显示书架面板并刷新）"""
        self.bookshelf_dock.show()
        self.refresh_bookmark_list()

    def show_about_dialog(self):
        """显示关于对话框"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于 喜阅",
            "<h2>📖 木木和叶子的喜阅</h2>"
            "<p>版本：2026.5</p>"
            "<hr>"
            "<p>一款本地小说阅读器，让阅读更愉悦。</p>"
            "<p>支持多种格式、书签管理、自动滚屏、翻页动画。</p>"
            "<hr>"
            "<p style='color: #888;'>© 2026 木木和叶子</p>"
        )

def main():

    def resizeEvent(self, event):
        """窗口大小变化时自适应工具栏图标大小"""
        super().resizeEvent(event)
        # 自适应工具栏图标大小，根据窗口宽度动态调整
        if hasattr(self, "toolbar"):
            width = self.width()
            # 根据窗口宽度比例计算合适的图标大小
            # 窗口越大，图标越大；窗口越小，图标越小
            new_size = max(16, min(32, int(width / 60)))
            self.toolbar.setIconSize(QSize(new_size, new_size))
    app = QApplication(sys.argv)
    window = NovelReaderMainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()