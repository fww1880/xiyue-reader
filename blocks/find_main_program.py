import os
# 列出novel_reader目录
print("novel_reader目录文件：")
for file in os.listdir('novel_reader'):
    print(f"  {file}")
# 查找主文件
main_files = []
for root, dirs, files in os.walk('novel_reader'):
    for file in files:
        if file.endswith('.py'):
            full_path = os.path.join(root, file)
            print(f"  {full_path}")
            if 'main' in file.lower():
                main_files.append(full_path)
utils.set_state(success=True, main_files=main_files)