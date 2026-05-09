import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查找文件过滤器和文件处理相关代码
txt_support = False
for i, line in enumerate(lines):
    if '.txt' in line:
        txt_support = True
        print(f"Line {i+1}: {line.strip()}")
if txt_support:
    print("✅ 程序支持打开 txt 文件")
else:
    print("❌ 未找到 txt 支持")