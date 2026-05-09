import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 查找书架列表相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'bookshelf' in line.lower() or 'book_list' in line.lower() or '书架' in line:
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找书签列表相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'bm_list' in line.lower() or 'bookmark_list' in line.lower() or '书签' in line:
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找右键菜单相关代码：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'context' in line.lower() or 'right' in line.lower() or '右键' in line or 'menu' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
print()
print("=" * 60)
print("🔍 查找删除相关方法：")
print("=" * 60)
for i, line in enumerate(lines, 1):
    if 'def delete' in line.lower() or 'def remove' in line.lower():
        print(f"  L{i}: {line.rstrip()}")
        for j in range(i, min(len(lines), i+15)):
            print(f"    L{j+1}: {lines[j].rstrip()}")
        print()