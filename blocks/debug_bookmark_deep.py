import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 1. 检查 add_bookmark 方法
print("🔍 检查 add_bookmark 方法中的保存逻辑：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def add_bookmark(self):' in line:
        in_method = True
        print(f"\nL{i}: {line.strip()}")
        continue
    if in_method:
        print(f"L{i}: {line.strip()}")
        if 'save_bookmarks' in line:
            print("  👆 调用了保存书签")
        if line.strip().startswith('def ') and 'add_bookmark' not in line:
            break
# 2. 检查 save_bookmarks 方法
print("\n\n🔍 检查 save_bookmarks 方法：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def save_bookmarks(self):' in line:
        in_method = True
        print(f"\nL{i}: {line.strip()}")
        continue
    if in_method:
        print(f"L{i}: {line.strip()}")
        if line.strip().startswith('def ') and 'save_bookmarks' not in line:
            break
# 3. 检查 load_bookmarks 方法
print("\n\n🔍 检查 load_bookmarks 方法：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def load_bookmarks(self):' in line:
        in_method = True
        print(f"\nL{i}: {line.strip()}")
        continue
    if in_method:
        print(f"L{i}: {line.strip()}")
        if line.strip().startswith('def ') and 'load_bookmarks' not in line:
            break
# 4. 检查 load_book 方法中是否调用了 load_bookmarks
print("\n\n🔍 检查 load_book 方法中是否加载书签：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def load_book(self' in line or 'def load_book(' in line:
        in_method = True
        print(f"\nL{i}: {line.strip()}")
        continue
    if in_method:
        print(f"L{i}: {line.strip()}")
        if 'load_bookmarks' in line or 'bookmark' in line:
            print("  👆 加载书签相关")
        if line.strip().startswith('def ') and 'load_book' not in line:
            break