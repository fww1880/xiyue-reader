import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 书架面板完整布局代码（行200-260）：")
print("=" * 60)
for i in range(199, min(260, len(lines))):
    print(f"L{i+1:4d}: {lines[i].rstrip()}")
print("=" * 60)
# 检查是否包含书签相关
has_bm = False
for i in range(199, 260):
    if 'bm_label' in lines[i] or 'bm_list_widget' in lines[i]:
        has_bm = True
        print(f"✅ 书签代码在 L{i+1}")
if not has_bm:
    print("❌ 书架布局中完全没有书签代码！")