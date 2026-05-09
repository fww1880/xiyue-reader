import os
# 读取阅读器要求文件
req_file = r"E:\AiPyPro\fww\阅读器要求.txt"
if os.path.exists(req_file):
    with open(req_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print("📋 阅读器要求内容：")
    print(content[:3000])
else:
    print(f"❌ 找不到要求文件: {req_file}")
# 查看novel_reader目录结构
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
print(f"\n📁 阅读器目录结构：")
for root, dirs, files in os.walk(novel_reader_dir):
    level = root.replace(novel_reader_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')