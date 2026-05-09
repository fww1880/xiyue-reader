import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 添加 resource_path 函数（处理 PyInstaller 路径）
resource_func = '''
import sys
import os
def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
'''
# 检查是否已存在
if 'def resource_path' not in content:
    # 在 import 区域后插入
    import_end = content.find('class ')
    if import_end > 0:
        content = content[:import_end] + resource_func + '\n' + content[import_end:]
        print("✅ 已添加 resource_path 函数")
# 2. 修改图标加载路径
old_icon_line = "icon_path = os.path.join(os.path.dirname(__file__), 'book_icon.ico')"
new_icon_line = "icon_path = resource_path('book_icon.ico')"
if old_icon_line in content:
    content = content.replace(old_icon_line, new_icon_line)
    print("✅ 已更新图标路径为 resource_path 模式")
else:
    # 尝试查找其他可能的图标路径设置
    import re
    # 查找 setWindowIcon 附近的 icon_path 定义
    matches = list(re.finditer(r'icon_path\s*=.*?book_icon\.ico', content, re.DOTALL))
    if matches:
        for m in matches:
            content = content.replace(m.group(), new_icon_line)
        print("✅ 已替换所有 book_icon.ico 路径引用")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 代码修改已保存")