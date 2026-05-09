import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 定义新的工具栏方法
new_tool_bar_code = '''    def create_tool_bar(self):
        """创建工具栏 - 马卡龙风格"""
        toolbar = self.addToolBar("主工具栏")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(28, 28)) # 图标大一点
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 文字在图标下方
        
        # 马卡龙配色样式表 (CSS)
        macaron_css = """
            QToolBar {
                background-color: #FFF0F5; /* 薰衣草红背景 (淡粉) */
                border-bottom: 3px solid #FFB7B2; /* 底部深粉边框 */
                padding: 6px;
                spacing: 12px;
            }
            QToolButton {
                background-color: #FFFFFF;
                border: 2px solid #AEC6CF; /* 马卡龙蓝边框 */
                border-radius: 12px;
                padding: 8px 14px;
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
        self.auto_scroll_action.triggered.connect(self.toggle_auto_scroll)
        toolbar.addAction(self.auto_scroll_action)
        
        # 专注模式
        focus_action = QAction("🧘 专注", self)
        focus_action.triggered.connect(self.toggle_focus_mode)
        toolbar.addAction(focus_action)
'''
# 查找旧方法并替换
start = content.find('    def create_tool_bar(self):')
if start != -1:
    # 找到下一个方法定义的开始位置
    end = content.find('\n    def ', start + 10)
    if end != -1:
        content = content[:start] + new_tool_bar_code + content[end:]
        print("✅ 工具栏样式已更新为马卡龙风格！")
    else:
        print("❌ 未找到方法结束位置")
else:
    print("❌ 未找到 create_tool_bar 方法")
# 保存文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)