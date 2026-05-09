import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
file_handler = os.path.join(novel_reader_dir, 'file_handler.py')
with open(file_handler, 'r', encoding='utf-8') as f:
    content = f.read()
print("📄 file_handler.py 完整内容：")
print(content)