import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 搜索 export_notes 相关行...")
for i, line in enumerate(lines):
    if 'export_notes' in line:
        print(f"L{i+1}: {line.rstrip()}")
# 修复行 378
if 'export_notes_action' in lines[377]:
    print(f"✅ 找到目标行 L378: {lines[377].rstrip()}")
    # 删除这三行
    del lines[377:380]
    print("✅ 已删除 export_notes 相关3行")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)