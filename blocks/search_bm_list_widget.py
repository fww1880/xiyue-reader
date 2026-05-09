import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 搜索 bm_list_widget 的创建和使用：")
for i, line in enumerate(lines):
    if 'bm_list_widget' in line:
        print(f"L{i+1}: {line.rstrip()}")