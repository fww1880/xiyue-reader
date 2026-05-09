import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 替换图标路径：从 icon.svg 改为 book_icon.ico
old_icon = "icon_path = os.path.join(os.path.dirname(__file__), 'icon.svg')"
new_icon = "icon_path = os.path.join(os.path.dirname(__file__), 'book_icon.ico')"
if old_icon in content:
    content = content.replace(old_icon, new_icon)
    print("✅ 已将图标路径从 icon.svg 改为 book_icon.ico")
else:
    print("⚠️ 未找到精确匹配，尝试模糊替换...")
    if "icon.svg" in content:
        content = content.replace("icon.svg", "book_icon.ico")
        print("✅ 已模糊替换图标文件名")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 修改已保存！")
# 验证修改结果
print("\n📋 验证修改后的代码片段：")
idx = content.find('icon_path =')
if idx >= 0:
    print(content[idx:idx+120])
idx2 = content.find('setWindowTitle')
if idx2 >= 0:
    print(content[idx2:idx2+100])