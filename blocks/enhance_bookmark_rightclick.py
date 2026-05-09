import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 修改文本区域右键菜单，添加"添加书签" =====
# 在 __init__ 中启用右键菜单
old_init_end = '''        # 自动滚屏定时器
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.do_auto_scroll)'''
new_init_end = '''        # 自动滚屏定时器
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.do_auto_scroll)
        
        # 添加右键菜单
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_text_context_menu)'''
content = content.replace(old_init_end, new_init_end)
# ===== 2. 添加右键菜单方法 =====
context_menu_method = '''
    def show_text_context_menu(self, pos):
        """文本区域右键菜单"""
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        # 添加书签
        add_bm_action = menu.addAction("🔖 添加书签到当前位置")
        add_bm_action.triggered.connect(self.add_bookmark)
        # 打开书签管理
        list_bm_action = menu.addAction("📋 管理书签")
        list_bm_action.triggered.connect(self.show_bookmark_list)
        # 显示菜单
        menu.exec_(self.text_edit.mapToGlobal(pos))
'''
# 在 add_bookmark 方法之前插入
pos = content.find('    def add_bookmark(self):')
if pos != -1:
    content = content[:pos] + context_menu_method + content[pos:]
    print("✅ 右键菜单方法已添加")
else:
    print("❌ 未找到 add_bookmark 方法")
# ===== 3. 修改书签列表点击跳转 =====
old_bm_list = '''        self.bm_list_widget = QListWidget()
        self.refresh_bookmark_list()
        layout.addWidget(self.bm_list_widget)'''
new_bm_list = '''        self.bm_list_widget = QListWidget()
        self.refresh_bookmark_list()
        # 单击即可跳转
        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))
        layout.addWidget(self.bm_list_widget)'''
content = content.replace(old_bm_list, new_bm_list)
print("✅ 书签列表单击跳转已启用")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("🚀 修改完成！")