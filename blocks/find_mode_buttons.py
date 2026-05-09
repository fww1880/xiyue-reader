import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找白天/夜间/护眼相关代码
print("🔍 查找阅读模式相关代码：")
for i, line in enumerate(lines, 1):
    if '白天' in line or '夜间' in line or '护眼' in line:
        print(f"L{i}: {line.strip()}")
    # 查找背景颜色设置
    if 'background_color' in line and ('white' in line or 'black' in line or 'green' in line or '#FFE4C4' in line):
        print(f"L{i}: {line.strip()}")
    # 查找切换方法
    if 'def set_' in line and ('background' in line or 'mode' in line):
        print(f"L{i}: {line.strip()}")