import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找窗口标题设置
import re
# 查找 setWindowTitle 或 setWindowIcon 相关代码
title_matches = list(re.finditer(r'setWindowTitle\([^)]+\)', content))
icon_matches = list(re.finditer(r'setWindowIcon\([^)]+\)', content))
print("🔍 当前窗口标题设置：")
for m in title_matches:
    start = max(0, m.start()-50)
    end = min(len(content), m.end()+50)
    print(f"  位置 {m.start()}: ...{content[start:end].strip()}...")
print("\n🔍 当前窗口图标设置：")
for m in icon_matches:
    start = max(0, m.start()-50)
    end = min(len(content), m.end()+50)
    print(f"  位置 {m.start()}: ...{content[start:end].strip()}...")
# 如果没有找到，也找一下类定义和 __init__
if not title_matches:
    print("\n⚠️ 未找到 setWindowTitle，查找主窗口类名...")
    class_matches = re.finditer(r'class\s+(\w+).*?:', content)
    for m in class_matches:
        print(f"  类定义: {m.group()}")