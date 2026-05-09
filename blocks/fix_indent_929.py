import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 检查第 925-935 行...")
for i in range(924, min(935, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
# 找到缩进问题并修复
if len(lines) >= 929:
    line = lines[928]
    if line.strip() and not line.startswith('    '):
        lines[928] = '    ' + line.lstrip()
        print("✅ 已修复缩进")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)