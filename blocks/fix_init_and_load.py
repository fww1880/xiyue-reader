import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 在 __init__ 中初始化 toc_label
old_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.toc_list = QListWidget()
        self.chapter_positions = []'''
new_init_vars = '''        self.current_theme = "day"  # day, night, eye_care
        self.toc_list = QListWidget()
        self.toc_label = QLabel("目录")
        self.chapter_positions = []'''
content = content.replace(old_init_vars, new_init_vars)
# 确保 load_book 中打开文件时也显示目录
old_load_book = '''            # 解析目录并生成目录面板
            self.build_table_of_contents(content, is_html)'''
new_load_book = '''            # 解析目录并生成目录面板
            self.build_table_of_contents(content, is_html)
            # 确保目录显示在书架面板
            self.toc_label.show()
            self.toc_list.show()'''
content = content.replace(old_load_book, new_load_book)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("补充修复完成！")
print("1. 在 __init__ 中初始化 toc_label")
print("2. load_book 中打开文件时确保目录显示")