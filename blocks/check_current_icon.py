import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
main_file = os.path.join(novel_reader_dir, 'main.py')
print(f"当前图标文件路径：{icon_path}")
print(f"图标文件是否存在：{os.path.exists(icon_path)}")
print(f"图标文件大小：{os.path.getsize(icon_path)} bytes")
# 检查代码中的图标引用
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找图标相关代码
icon_refs = []
if 'book_icon.ico' in content:
    icon_refs.append('book_icon.ico')
if 'icon' in content.lower():
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'icon' in line.lower():
            icon_refs.append(f"Line {i+1}: {line.strip()}")
print(f"\n代码中图标引用：")
for ref in icon_refs:
    print(ref)