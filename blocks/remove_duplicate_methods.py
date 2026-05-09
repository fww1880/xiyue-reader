import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 删除 L914-L998 之间的旧方法块（show_bookmarks, jump_to_bookmark, 导出）
old_block_start = content.find('    def show_bookmarks(self):')
old_block_end = content.find('    def add_bookmark(self):', old_block_start + 1)
if old_block_start != -1 and old_block_end != -1:
    old_block = content[old_block_start:old_block_end]
    content = content.replace(old_block, '')
    print(f"✅ 已删除旧方法块（show_bookmarks, jump_to_bookmark 等）")
# 删除 L1001-L1026 之间的第二个 add_bookmark
second_add = content.find('    def add_bookmark(self):', old_block_end)
if second_add != -1:
    second_add_end = content.find('\n    def ', second_add + 1)
    if second_add_end != -1:
        old_second = content[second_add:second_add_end]
        content = content.replace(old_second, '')
        print("✅ 已删除第二个 add_bookmark 方法")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("🚀 重复方法已清理完成！")