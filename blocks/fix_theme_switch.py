import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 apply_theme 方法
old_apply_theme = '''    def apply_theme(self):
        """应用主题配色"""
        palette = QPalette()
        
        if self.current_theme == "day":
            bg_color = QColor(255, 255, 255)
            text_color = QColor(0, 0, 0)
        elif self.current_theme == "night":
            bg_color = QColor(20, 20, 30)
            text_color = QColor(200, 200, 200)
        elif self.current_theme == "eye_care":
            bg_color = QColor(204, 232, 207)
            text_color = QColor(0, 0, 0)
        else:
            bg_color = QColor(255, 255, 255)
            text_color = QColor(0, 0, 0)
            
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.Base, bg_color)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.WindowText, text_color)
        
        self.text_edit.setPalette(palette)
        self.setPalette(palette)'''
new_apply_theme = '''    def apply_theme(self):
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
        self.status_bar.showMessage(f"已切换至{'白天' if self.current_theme=='day' else '夜间' if self.current_theme=='night' else '护眼'}模式", 2000)'''
if old_apply_theme in content:
    content = content.replace(old_apply_theme, new_apply_theme)
    print("✅ 成功替换 apply_theme 方法，改用 setStyleSheet 确保生效")
else:
    print("⚠️ 未找到完全匹配的旧方法，尝试按行替换...")
    # 备用方案：如果字符串不完全匹配，尝试定位函数并替换
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if 'def apply_theme(self):' in line:
            start_idx = i
        if start_idx is not None and i > start_idx:
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                end_idx = i
                break
    if start_idx is not None:
        # 找到方法体，进行替换
        new_lines = lines[:start_idx] + new_apply_theme.split('\n') + lines[end_idx:]
        content = '\n'.join(new_lines)
        print("✅ 按行替换成功")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存修改")