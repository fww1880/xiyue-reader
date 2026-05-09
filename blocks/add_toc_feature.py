import os
main_path = os.path.join(os.getcwd(), 'novel_reader', 'main.py')
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
# ========== 1. 在 import 部分添加 QSplitter（如果还没有） ==========
if 'QSplitter' not in content:
    # 已经导入了，跳过
    pass
# ========== 2. 在 __init__ 中添加目录面板 ==========
old_init_end = """        self.setWindowTitle("本地小说阅读器")
        self.resize(1200, 800)"""
new_init_add = """        self.setWindowTitle("本地小说阅读器")
        self.resize(1200, 800)
        
        # 目录面板
        self.toc_list = QListWidget()
        self.toc_list.setMaximumWidth(250)
        self.toc_list.setMinimumWidth(180)
        self.toc_list.setFont(QFont("Microsoft YaHei", 10))
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        self.toc_list.hide()  # 默认隐藏，打开书时显示
        
        # 章节位置缓存
        self.chapter_positions = []  # [(title, cursor_position), ...]
        
        # 将目录面板和文本编辑器放入水平布局
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        
        # 主内容区用 QSplitter 左右分割
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.toc_list)
        self.splitter.addWidget(self.text_edit)
        self.splitter.setStretchFactor(0, 0)  # 目录不拉伸
        self.splitter.setStretchFactor(1, 1)  # 文本区域拉伸"""
content = content.replace(old_init_end, new_init_add)
# ========== 3. 移除旧的 self.text_edit 创建（因为上面已经创建了） ==========
old_text_edit_create = """        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Microsoft YaHei", 12))
        self.text_edit.setStyleSheet(\"\"\"
            QTextEdit {
                background-color: #F5F0E8;
                color: #333333;
                padding: 20px;
                border: none;
            }
        \"\"\")"""
new_text_edit_create = """        self.text_edit.setFont(QFont("Microsoft YaHei", 12))
        self.text_edit.setStyleSheet(\"\"\"
            QTextEdit {
                background-color: #F5F0E8;
                color: #333333;
                padding: 20px;
                border: none;
            }
        \"\"\")"""
content = content.replace(old_text_edit_create, new_text_edit_create)
# ========== 4. 替换中心部件设置 ==========
old_central = """        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_edit)"""
new_central = """        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.splitter)"""
content = content.replace(old_central, new_central)
# ========== 5. 修改 load_book 方法，添加目录解析 ==========
old_load_book = """    def load_book(self, file_path):
        \"\"\"加载书籍文件\"\"\"
        try:
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
            self.setWindowTitle(f"本地小说阅读器 - {os.path.basename(file_path)}")
            
            # 恢复上次阅读位置
            position = self.settings.value(f"position_{file_path}", 0, int)
            if position > 0 and position < len(content):
                cursor = self.text_edit.textCursor()
                cursor.setPosition(position)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                
            QMessageBox.information(self, "成功", f"成功加载文件：{os.path.basename(file_path)}")
        except Exception as e:
            # 双层保护，绝对不闪退
            error_msg = f"加载文件失败：{str(e)}\\n\\n请检查文件是否存在、损坏或格式不支持。\"
            try:
                QMessageBox.critical(self, "错误", error_msg)
            except:
                # 如果连弹窗都失败了，至少保证不崩溃
                print(error_msg)"""
new_load_book = """    def load_book(self, file_path):
        \"\"\"加载书籍文件\"\"\"
        try:
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
            self.setWindowTitle(f"本地小说阅读器 - {os.path.basename(file_path)}")
            
            # 解析目录并生成目录面板
            self.build_table_of_contents(content, is_html)
            
            # 恢复上次阅读位置
            position = self.settings.value(f"position_{file_path}", 0, int)
            if position > 0 and position < len(content):
                cursor = self.text_edit.textCursor()
                cursor.setPosition(position)
                self.text_edit.setTextCursor(cursor)
                self.text_edit.ensureCursorVisible()
                
            QMessageBox.information(self, "成功", f"成功加载文件：{os.path.basename(file_path)}")
        except Exception as e:
            # 双层保护，绝对不闪退
            error_msg = f"加载文件失败：{str(e)}\\n\\n请检查文件是否存在、损坏或格式不支持。\"
            try:
                QMessageBox.critical(self, "错误", error_msg)
            except:
                # 如果连弹窗都失败了，至少保证不崩溃
                print(error_msg)"""
content = content.replace(old_load_book, new_load_book)
# ========== 6. 添加 build_table_of_contents 和 jump_to_chapter 方法 ==========
# 找插入位置：在 load_book 方法之后
insert_point = content.find('def load_book')
# 找到 load_book 方法结束位置
after_load_book = content.find('\n    def ', insert_point + 10)
if after_load_book == -1:
    after_load_book = content.find('\n    # ', insert_point + 10)
if after_load_book == -1:
    after_load_book = content.find('\nclass ', insert_point + 10)
new_methods = """
    def build_table_of_contents(self, content, is_html):
        \"\"\"解析文本内容，生成目录列表\"\"\"
        import re
        
        self.toc_list.clear()
        self.chapter_positions = []
        
        if is_html:
            # HTML格式：匹配<h1>-<h6>标签作为章节
            pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                pos = match.start()
                if title:
                    self.chapter_positions.append((title, pos))
        else:
            # 纯文本格式：匹配常见章节标题
            # 支持格式：第X章、第X节、第X卷、Chapter X、Ch.X、数字序号章节等
            patterns = [
                r'^\\s*第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集]\\s*.*$',  # 第一章、第二节、第三卷
                r'^\\s*[\\[【（(]?第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集][\\]】）)]?\\s*.*$',  # 【第一章】等
                r'^\\s*(?:Chapter|Ch|Section|Part|Volume)\\s*[0-9IVXLCDM]+[.:、\\s].*$',  # Chapter 1、Part I
                r'^\\s*[\\[【（(]?[0-9]+[、.．\\s}])].*$',  # 1.、1、1)
                r'^\\s*[\\[【（(]?[0-9]+[\\]】）)]\\s*.*$',  # [1]、【1】
                r'^\\s*[\\[【（(]?[零一二三四五六七八九十百千万]+[、.．\\s}])].*$',  # 一、一.
            ]
            
            lines = content.split('\\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped:
                    continue
                for pat in patterns:
                    if re.match(pat, stripped, re.IGNORECASE):
                        # 计算这个章节在全文中的字符位置
                        char_pos = sum(len(l) + 1 for l in lines[:i])
                        self.chapter_positions.append((stripped, char_pos))
                        break
        
        # 填充目录列表
        if self.chapter_positions:
            for title, pos in self.chapter_positions:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, pos)
                self.toc_list.addItem(item)
            self.toc_list.show()
            self.toc_list.setMinimumWidth(200)
        else:
            self.toc_list.hide()
    
    def jump_to_chapter(self, item):
        \"\"\"点击目录项，跳转到对应章节位置\"\"\"
        pos = item.data(Qt.UserRole)
        if pos is not None:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(pos)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.ensureCursorVisible()
            self.text_edit.setFocus()
"""
content = content[:after_load_book] + new_methods + content[after_load_book:]
# ========== 7. 写入文件 ==========
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 目录章节导航功能添加完成！")
print("修改内容：")
print("1. 添加右侧目录面板 (QListWidget)")
print("2. 解析章节标题：支持'第X章'、'Chapter X'、数字序号等多种格式")
print("3. 点击目录项自动跳转到对应章节位置")
print("4. 无目录时自动隐藏面板")