import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 1. 检查 import_folder 方法中是否更新了 bookshelf_data
print("🔍 检查 import_folder 方法中是否保存书库数据：")
in_import = False
for i, line in enumerate(lines, 1):
    if 'def import_folder' in line:
        in_import = True
        print(f"\nL{i}: {line.strip()}")
    elif in_import:
        print(f"L{i}: {line.strip()}")
        if 'bookshelf_data' in line:
            print("  👆 找到 bookshelf_data 相关代码")
        if line.strip().startswith('def ') and 'import_folder' not in line:
            break
# 2. 检查 on_close 方法
print("\n\n🔍 检查 on_close 方法中的保存逻辑：")
in_on_close = False
for i, line in enumerate(lines, 1):
    if 'def on_close' in line:
        in_on_close = True
        print(f"\nL{i}: {line.strip()}")
    elif in_on_close:
        print(f"L{i}: {line.strip()}")
        if 'bookshelf_data' in line or 'save_bookmarks' in line:
            print("  👆 关键保存代码")
        if line.strip().startswith('def ') and 'on_close' not in line:
            break
# 3. 检查 restore_state 方法
print("\n\n🔍 检查 restore_state 方法中的恢复逻辑：")
in_restore = False
for i, line in enumerate(lines, 1):
    if 'def restore_state' in line:
        in_restore = True
        print(f"\nL{i}: {line.strip()}")
    elif in_restore:
        print(f"L{i}: {line.strip()}")
        if 'bookshelf_data' in line or 'saved_books' in line:
            print("  👆 关键恢复代码")
        if line.strip().startswith('def ') and 'restore_state' not in line:
            break