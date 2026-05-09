import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到第二个 add_bookmark
first = content.find('def add_bookmark')
second = content.find('def add_bookmark', first + 1)
if second != -1:
    second_end = content.find('\n    def ', second + 1)
    if second_end == -1:
        second_end = len(content)
    old_method = content[second:second_end]
    content = content.replace(old_method, '')
    print("✅ 已删除第二个 add_bookmark 方法")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("✅ 只有一个 add_bookmark 方法")