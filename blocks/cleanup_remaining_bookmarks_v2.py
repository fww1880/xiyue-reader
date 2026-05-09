import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 逐行替换所有 self.bookmarks -> self.bookmark_list
new_lines = []
count = 0
for line in lines:
    if 'self.bookmarks' in line and 'bookmark_list' not in line:
        new_line = line.replace('self.bookmarks', 'self.bookmark_list')
        new_lines.append(new_line)
        count += 1
    else:
        new_lines.append(line)
print(f"✅ 清理了 {count} 处残留的 self.bookmarks")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("🚀 彻底清理完成！所有地方都使用 self.bookmark_list 了！")