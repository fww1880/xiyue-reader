import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 搜索所有包含 bookmark 的行：")
print("=" * 70)
for i, line in enumerate(lines):
    if 'bookmark' in line.lower() or '书签' in line:
        print(f"L{i+1:4d}: {line.rstrip()}")
print("=" * 70)
# 统计
count_bookmarks = sum(1 for l in lines if 'self.bookmarks' in l)
count_bookmark_list = sum(1 for l in lines if 'self.bookmark_list' in l)
count_settings = sum(1 for l in lines if 'bookmarks_' in l)
print(f"\n📊 统计：")
print(f"  self.bookmarks 出现: {count_bookmarks} 次")
print(f"  self.bookmark_list 出现: {count_bookmark_list} 次")
print(f"  bookmarks_ (settings) 出现: {count_settings} 次")
```
<!-- Block-Start: {"name": "full_code_search_bookmarks", "path": "full_code_search_bookmarks.py"} -->
```python
import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 搜索所有包含 bookmark 的行：")
print("=" * 70)
for i, line in enumerate(lines):
    if 'bookmark' in line.lower() or '书签' in line:
        print(f"L{i+1:4d}: {line.rstrip()}")
print("=" * 70)
# 统计
count_bookmarks = sum(1 for l in lines if 'self.bookmarks' in l)
count_bookmark_list = sum(1 for l in lines if 'self.bookmark_list' in l)
count_settings = sum(1 for l in lines if 'bookmarks_' in l)
print(f"\n📊 统计：")
print(f"  self.bookmarks 出现: {count_bookmarks} 次")
print(f"  self.bookmark_list 出现: {count_bookmark_list} 次")
print(f"  bookmarks_ (settings) 出现: {count_settings} 次")