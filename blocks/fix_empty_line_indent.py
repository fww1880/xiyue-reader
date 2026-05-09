import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# L928 是空行，L929 是方法定义，需要删除空行或调整缩进
if len(lines) >= 929:
    # 检查 L928 是否是空行
    if lines[928].strip() == '':
        # 删除空行
        del lines[928]
        print("✅ 已删除 L929 前的空行")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)