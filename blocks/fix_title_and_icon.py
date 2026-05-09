import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修复打开文件后的标题 - 把 "本地小说阅读器 - xxx" 改成 "喜阅 - xxx"
old_open_title = '''self.setWindowTitle(f"本地小说阅读器 - {os.path.basename(file_path)}")'''
new_open_title = '''self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")'''
if old_open_title in content:
    content = content.replace(old_open_title, new_open_title)
    print("✅ 已修改打开文件后的窗口标题：喜阅 - xxx")
else:
    print("⚠️ 未找到打开文件后的标题设置，尝试模糊匹配...")
    if '本地小说阅读器' in content:
        content = content.replace('本地小说阅读器', '喜阅')
        print("✅ 已通过模糊替换修改标题")
# 2. 确认图标路径设置正确（使用我们生成的 book_icon.ico）
# 查找图标设置代码
icon_pattern = r'self\.setWindowIcon\(QIcon\(icon_path\)\)'
if re.search(icon_pattern, content):
    # 检查 icon_path 的定义
    icon_def_pattern = r'icon_path\s*='
    icon_defs = list(re.finditer(icon_def_pattern, content))
    if icon_defs:
        # 找到最后一个 icon_path 定义（在 init_ui 中的）
        for m in icon_defs:
            start = m.start()
            end = min(len(content), start + 100)
            print(f"📌 icon_path 定义位置 {start}: {content[start:end].strip()}")
    
    # 检查是否直接使用了 book_icon.ico
    if 'book_icon.ico' not in content:
        print("⚠️ 未找到直接使用 book_icon.ico，检查当前图标路径设置...")
        # 查找 icon_path 赋值
        icon_assign = re.search(r'icon_path\s*=\s*["\']([^"\']+)["\']', content)
        if icon_assign:
            print(f"  当前图标路径: {icon_assign.group(1)}")
            # 如果路径不对，替换为正确的
            if 'book_icon.ico' not in icon_assign.group(1):
                # 替换为正确的路径
                old_path = icon_assign.group(0)
                new_path = f'icon_path = os.path.join(os.path.dirname(__file__), "book_icon.ico")'
                content = content.replace(old_path, new_path)
                print("✅ 已更新图标路径为 book_icon.ico")
    else:
        print("✅ 图标路径已正确指向 book_icon.ico")
else:
    print("⚠️ 未找到 setWindowIcon 调用，需要添加")
# 保存修改
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n✅ 所有修改已保存！")