import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 1. 添加键盘快捷键处理 =====
# 在 init_ui 中启用键盘事件
old_init_ui = '''        # 创建状态栏
        self.status_bar = QStatusBar()
        self.position_label = QLabel("进度：0%")
        self.status_bar.addWidget(self.position_label)
        self.setStatusBar(self.status_bar)
        
        # 自动滚屏定时器'''
new_init_ui = '''        # 创建状态栏
        self.status_bar = QStatusBar()
        self.position_label = QLabel("进度：0%")
        self.status_bar.addWidget(self.position_label)
        self.setStatusBar(self.status_bar)
        
        # 启用键盘快捷键
        self.text_edit.keyPressEvent = self.keyboard_pagination
        
        # 自动滚屏定时器'''
content = content.replace(old_init_ui, new_init_ui)
# ===== 2. 添加键盘翻页方法 =====
keyboard_method = '''    def keyboard_pagination(self, event):
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
        """上一页"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        scrollbar.setValue(current - page_size)
    
    def next_page(self):
        """下一页"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        scrollbar.setValue(current + page_size)'''
# 在 init_ui 方法前插入键盘翻页方法
content = content.replace('    def init_ui(self):', keyboard_method + '\n    def init_ui(self):')
# ===== 3. 添加鼠标滚轮翻页 =====
wheel_method = '''    def wheel_event(self, event):
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
        event.accept()'''
# 在 keyboard_pagination 后插入 wheel_event
content = content.replace('    def keyboard_pagination(self, event):', keyboard_method + '\n    def wheel_event(self, event):')
# 但上面已经替换了，需要调整。实际上，我先插入 keyboard_method，然后插入 wheel_method
# 重新组织：先插入两个方法，再修改 init_ui
# 这里有点复杂，我简化一下：直接在所有方法最后添加
# 查找最后一个方法
last_method_start = content.find('\n    def ')
if last_method_start != -1:
    # 在最后一个方法前插入
    content = content[:last_method_start] + keyboard_method + '\n' + wheel_method + '\n' + content[last_method_start:]
# ===== 4. 添加工具栏翻页按钮 =====
# 修改 create_tool_bar 方法
old_toolbar = '''    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)'''
new_toolbar = '''    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 翻页按钮
        prev_action = QAction("上一页", self)
        prev_action.setShortcut("Ctrl+Left")
        prev_action.triggered.connect(self.prev_page)
        toolbar.addAction(prev_action)
        
        next_action = QAction("下一页", self)
        next_action.setShortcut("Ctrl+Right")
        next_action.triggered.connect(self.next_page)
        toolbar.addAction(next_action)
        
        toolbar.addSeparator()
        
        # 自动滚屏按钮
        auto_scroll_action = QAction("自动滚屏", self)
        auto_scroll_action.setCheckable(True)
        auto_scroll_action.triggered.connect(self.toggle_auto_scroll)
        toolbar.addAction(auto_scroll_action)'''
if old_toolbar in content:
    content = content.replace(old_toolbar, new_toolbar)
# ===== 5. 添加自动滚屏控制方法 =====
auto_scroll_method = '''    def toggle_auto_scroll(self):
        """切换自动滚屏"""
        self.auto_scroll_enabled = not self.auto_scroll_enabled
        if self.auto_scroll_enabled:
            self.auto_scroll_timer.start(1000 // self.auto_scroll_speed)
        else:
            self.auto_scroll_timer.stop()
    
    def do_auto_scroll(self):
        """执行自动滚屏"""
        if self.auto_scroll_enabled:
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(scrollbar.value() + 1)'''
# 插入自动滚屏方法
content = content.replace('    def toggle_auto_scroll(self):', auto_scroll_method)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 翻页功能增强完成！")
print("新增功能：")
print("1. 键盘方向键翻页（上下左右、PageUp/PageDown、空格键）")
print("2. 鼠标滚轮翻页")
print("3. 工具栏翻页按钮（上一页/下一页）")
print("4. 自动滚屏开关")