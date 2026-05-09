import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 L925-L935 完整内容：")
for i in range(924, min(935, len(lines))):
    print(f"L{i+1}: {repr(lines[i])}")
# 手动修复：确保空行没有缩进
for i in range(924, min(935, len(lines))):
    if lines[i].strip() == '' and lines[i] != '\n':
        lines[i] = '\n'
        print(f"✅ 修复 L{i+1} 空行缩进")
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("🚀 空行缩进已修复")