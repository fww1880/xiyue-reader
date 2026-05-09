import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 删除 L927 和 L928 的空行
if len(lines) >= 929:
    if lines[927].strip() == '' and lines[928].strip() == '':
        del lines[927:929]
        print("✅ 已删除 L928-L929 的两个空行")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)