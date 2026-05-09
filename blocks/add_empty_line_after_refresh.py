import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 在 L945 后添加空行
lines.insert(945, '\n')
print("✅ 已在 L945 后添加空行")
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)