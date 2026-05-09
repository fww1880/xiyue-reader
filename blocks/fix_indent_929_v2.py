import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 检查 L925-L935 的缩进：")
for i in range(924, min(935, len(lines))):
    line = lines[i]
    leading = len(line) - len(line.lstrip())
    print(f"L{i+1}: leading={leading:2d} | {repr(line.rstrip())}")
# 修复 L929 的缩进
if len(lines) >= 929:
    line = lines[928]
    if line.strip().startswith('def ') and not line.startswith('    '):
        lines[928] = '    ' + line.lstrip()
        print("✅ 已修复 L929 缩进")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)