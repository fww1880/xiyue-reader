import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 在 refresh_bookmark_list 方法后添加 show_bookmark_list 方法
# 找到 refresh_bookmark_list 方法的结束位置
end_pos = None
for i in range(926, len(lines)):
    if lines[i].strip() and not lines[i].startswith('    '):
        end_pos = i
        break
if end_pos:
    # 在 end_pos 前插入新方法
    new_method = '''    def show_bookmark_list(self):
        """显示书签列表（显示书架面板并刷新）"""
        self.bookshelf_dock.show()
        self.refresh_bookmark_list()
'''
    lines.insert(end_pos, new_method)
    print(f"✅ 已在 L{end_pos+1} 添加 show_bookmark_list 方法")
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)