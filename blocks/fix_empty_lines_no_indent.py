import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 把 L927 和 L928 改成纯换行符
if len(lines) >= 929:
    lines[927] = '\n'
    lines[928] = '\n'
    print("✅ 已修复 L928-L929 空行为纯换行符")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)