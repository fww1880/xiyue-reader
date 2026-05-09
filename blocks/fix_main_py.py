import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修复：在 __init__ 中初始化 toc_list 和 chapter_positions
old_init = """        self.current_theme = "day"  # day, night, eye_care
        
        # 初始化UI
        self.init_ui()"""
new_init = """        self.current_theme = "day"  # day, night, eye_care
        self.toc_list = QListWidget()
        self.chapter_positions = []
        
        # 初始化UI
        self.init_ui()"""
content = content.replace(old_init, new_init)
# 2. 修复：在阅读面板中添加目录列表
old_reading = """        # 阅读文本区域
        self.text_edit = QTextEdit()"""
new_reading = """        # 目录列表（默认隐藏）
        self.toc_list = QListWidget()
        self.toc_list.setVisible(False)
        self.toc_list.itemClicked.connect(self.jump_to_chapter)
        reading_layout.addWidget(self.toc_list)
        
        # 阅读文本区域
        self.text_edit = QTextEdit()"""
content = content.replace(old_reading, new_reading)
# 写入修复后的内容
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ main.py 修复完成！")
print("修复内容：")
print("1. 在 __init__ 中初始化 toc_list 和 chapter_positions")
print("2. 在阅读面板中添加目录列表 QListWidget")