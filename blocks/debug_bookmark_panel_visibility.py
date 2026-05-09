import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 检查书架面板中的书签标签和列表...")
found_bm_label = False
found_bm_list = False
for i, line in enumerate(lines):
    if 'self.bm_label' in line:
        print(f"✅ 找到书签标签: L{i+1}: {line.strip()}")
        found_bm_label = True
    if 'self.bm_list_widget' in line:
        print(f"✅ 找到书签列表: L{i+1}: {line.strip()}")
        found_bm_list = True
if not found_bm_label:
    print("❌ 未找到书签标签，可能没添加到书架面板")
if not found_bm_list:
    print("❌ 未找到书签列表，可能没添加到书架面板")
print("\n🔍 检查书架面板布局...")
for i in range(200, 250):
    if 'bookshelf_layout' in lines[i]:
        print(f"L{i+1}: {lines[i].strip()}")