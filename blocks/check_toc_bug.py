import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 jump_to_chapter 方法
import re
# 提取 jump_to_chapter 方法
start = content.find('def jump_to_chapter')
end = content.find('\n    def ', start + 1)
if end == -1:
    end = len(content)
print("📄 jump_to_chapter 方法：")
print(content[start:end])
print("\n" + "="*50)
# 提取 build_table_of_contents 方法
start2 = content.find('def build_table_of_contents')
end2 = content.find('\n    def ', start2 + 1)
if end2 == -1:
    end2 = len(content)
print("📄 build_table_of_contents 方法：")
print(content[start2:end2])