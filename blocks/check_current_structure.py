import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("文件长度:", len(content))
print("包含'书架'的行:")
for i, line in enumerate(content.split('\n')):
    if '书架' in line or 'bookshelf' in line.lower():
        print(f"Line {i}: {line.strip()}")
print("包含'my_library'或'my_books'的行:")
for i, line in enumerate(content.split('\n')):
    if 'my_library' in line.lower() or 'my_books' in line.lower() or 'shelf' in line.lower():
        print(f"Line {i}: {line.strip()}")