import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找L300附近 toc_list 的样式
print("📋 目录列表框（toc_list）样式：")
for i in range(300, 320):
    if i < len(lines):
        print(f"L{i+1}: {lines[i].strip()}")
print("\n📋 书签列表框（bm_list_widget）样式：")
for i in range(315, 335):
    if i < len(lines):
        print(f"L{i+1}: {lines[i].strip()}")
# 查找L520附近书架区域样式
print("\n📋 书架区域样式（L520附近）：")
for i in range(520, 550):
    if i < len(lines):
        print(f"L{i+1}: {lines[i].strip()}")