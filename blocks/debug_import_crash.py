import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找 import_folder 方法完整内容
print("🔍 查看完整的 import_folder 方法：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def import_folder' in line:
        in_method = True
    if in_method:
        print(f"L{i}: {line.strip()}")
        if line.strip().startswith('def ') and 'import_folder' not in line:
            break