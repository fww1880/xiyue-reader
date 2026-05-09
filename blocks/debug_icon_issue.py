import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("=" * 60)
print("🔍 深度排查图标设置问题")
print("=" * 60)
# 1. 查找所有 setWindowIcon 调用
icon_calls = list(re.finditer(r'self\.setWindowIcon\(.*?\)', content))
print(f"\n📌 找到 {len(icon_calls)} 处 setWindowIcon 调用：")
for i, m in enumerate(icon_calls):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 50)
    context = content[start:end].replace('\n', ' ')
    print(f"  [{i+1}] 位置 {m.start()}: ...{context}...")
# 2. 查找 resource_path 定义和调用
rp_def = re.search(r'def resource_path\(.*?\):.*?return.*?relative_path.*?\)', content, re.DOTALL)
if rp_def:
    print(f"\n✅ resource_path 函数已定义")
else:
    print(f"\n❌ resource_path 函数未找到或定义不完整")
rp_calls = list(re.finditer(r'resource_path\(.*?\)', content))
print(f"\n📌 找到 {len(rp_calls)} 处 resource_path 调用：")
for i, m in enumerate(rp_calls):
    line_start = content.rfind('\n', 0, m.start()) + 1
    line_end = content.find('\n', m.end())
    if line_end == -1: line_end = len(content)
    print(f"  [{i+1}] {content[line_start:line_end].strip()}")
# 3. 检查 QIcon 导入
if 'from PyQt5.QtGui import QIcon' in content or 'import QIcon' in content:
    print("\n✅ QIcon 已导入")
else:
    print("\n⚠️ QIcon 可能未正确导入")
# 4. 检查 book_icon.ico 是否存在
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
if os.path.exists(icon_path):
    print(f"\n✅ 图标文件存在：{icon_path}")
    print(f"   大小：{os.path.getsize(icon_path)} bytes")
else:
    print(f"\n❌ 图标文件不存在：{icon_path}")
# 5. 输出 init_ui 方法中的图标设置代码
init_ui_match = re.search(r'def init_ui\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if init_ui_match:
    init_ui_code = init_ui_match.group()
    if 'setWindowIcon' in init_ui_code:
        print("\n📄 init_ui 中的图标设置代码：")
        lines = init_ui_code.split('\n')
        for line in lines:
            if 'setWindowIcon' in line or 'resource_path' in line or 'icon' in line.lower():
                print(f"  {line.strip()}")
    else:
        print("\n⚠️ init_ui 中未找到 setWindowIcon 调用")