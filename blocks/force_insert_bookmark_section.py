import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 在第247行（bookshelf_layout.addWidget(self.toc_list)）后面插入书签代码
insert_pos = 246  # 0-based index
# 书签代码块
bookmark_code = [
    '\n',
    '        # 书签标签\n',
    '        self.bm_label = QLabel("书签")\n',
    '        self.bm_label.setStyleSheet("font-weight: bold; color: #555;")\n',
    '        bookshelf_layout.addWidget(self.bm_label)\n',
    '\n',
    '        # 书签列表\n',
    '        self.bm_list_widget = QListWidget()\n',
    '        self.bm_list_widget.itemClicked.connect(lambda item: self.jump_to_selected_bookmark(None))\n',
    '        bookshelf_layout.addWidget(self.bm_list_widget)\n',
]
new_lines = lines[:insert_pos+1] + bookmark_code + lines[insert_pos+1:]
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("✅ 书签代码已强制插入书架布局！")
print(f"原文件 {len(lines)} 行 -> 新文件 {len(new_lines)} 行")