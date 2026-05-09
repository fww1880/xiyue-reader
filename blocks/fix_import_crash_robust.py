import os
import sys
import subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# Read current content
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# Fix 1: import_folder - Mark category items
target1 = 'category_item = QTreeWidgetItem(self.books_tree, [category_name])'
if target1 in content:
    content = content.replace(target1, target1 + '\n            category_item.setData(0, Qt.UserRole, "__category__")')
    print("✅ Fixed category_item")
else:
    print("⚠️ target1 not found")
target2 = 'sub_category = QTreeWidgetItem(category_item, [rel_path])'
if target2 in content:
    content = content.replace(target2, target2 + '\n                    sub_category.setData(0, Qt.UserRole, "__subcategory__")')
    print("✅ Fixed sub_category")
else:
    print("⚠️ target2 not found")
# Fix 2: open_book_from_tree - Skip category items
target3 = 'file_path = item.data(0, Qt.UserRole)'
if target3 in content:
    content = content.replace(target3, target3 + '\n        if not file_path or str(file_path).startswith("__"):\n            return')
    print("✅ Fixed open_book_from_tree")
else:
    print("⚠️ target3 not found")
# Save
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("🚀 Fixes applied. Restarting...")
# Kill old process
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'main.py' in ' '.join(cmdline) and 'novel_reader' in ' '.join(cmdline):
                proc.kill()
                print(f"  ✅ Killed PID: {proc.info['pid']}")
        except:
            pass
except:
    pass
# Start new process
try:
    process = subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ Reader started.")
except Exception as e:
    print(f"❌ Start failed: {e}")