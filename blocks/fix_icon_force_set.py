import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找并替换 init_ui 中的图标设置代码
old_icon_code = '''icon_path = resource_path('book_icon.ico')
        if os.path.exists(icon_path):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(resource_path('book_icon.ico')))'''
new_icon_code = '''# 强制设置窗口图标（移除 exists 检查，确保一定执行）
        try:
            from PyQt5.QtGui import QIcon
            icon_full_path = resource_path('book_icon.ico')
            self.setWindowIcon(QIcon(icon_full_path))
            print(f"✅ 窗口图标已设置：{icon_full_path}")
        except Exception as e:
            print(f"⚠️ 设置窗口图标失败：{e}")'''
if old_icon_code in content:
    content = content.replace(old_icon_code, new_icon_code)
    print("✅ 已替换图标设置代码（移除 exists 检查）")
else:
    print("⚠️ 未精确匹配，尝试模糊替换...")
    # 查找 setWindowIcon 附近的代码块
    match = re.search(r'icon_path\s*=\s*resource_path\(.*?\n.*?if os\.path\.exists.*?\n.*?setWindowIcon.*?\)', content, re.DOTALL)
    if match:
        content = content.replace(match.group(), new_icon_code)
        print("✅ 已模糊替换图标设置代码")
    else:
        # 直接替换 setWindowIcon 调用
        content = re.sub(
            r'self\.setWindowIcon\(QIcon\(resource_path\([^\)]+\)\)\)',
            "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))",
            content
        )
        print("✅ 已确保 setWindowIcon 调用正确")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")
# 验证
print("\n📋 验证修改后的代码：")
idx = content.find('强制设置窗口图标')
if idx >= 0:
    end = content.find('\n', idx + 200)
    if end > 0:
        print(content[idx:end])