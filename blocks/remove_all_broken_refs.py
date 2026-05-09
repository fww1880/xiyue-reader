import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 删除所有引用 show_about 的行
new_lines = []
deleted = []
for i, line in enumerate(lines):
    if 'show_about' in line or 'export_notes' in line:
        deleted.append(f"L{i+1}: {line.rstrip()}")
    else:
        new_lines.append(line)
print("🗑️ 删除的引用行：")
for d in deleted:
    print(f"  {d}")
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"✅ 已删除 {len(deleted)} 行无效引用")