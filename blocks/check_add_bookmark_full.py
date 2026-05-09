import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 L905-L935 完整内容（add_bookmark 方法）：")
for i in range(904, min(935, len(lines))):
    print(f"L{i+1}: {repr(lines[i])}")