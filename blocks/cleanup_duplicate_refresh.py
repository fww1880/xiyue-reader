import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 删除第488行（错误的缩进）
lines[487] = '            self.load_bookmarks()\n'
# 删除第489行（重复的）
lines[488] = '            self.refresh_bookmark_list() # 加载书签\n'
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("✅ 清理了重复和错误的 refresh 调用")