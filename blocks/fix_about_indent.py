import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 查看 L1178-1190 的精确内容
print("🔍 L1178-L1190 内容：")
for i in range(1177, 1191):
    if i < len(lines):
        print(f"  L{i+1}: {repr(lines[i])}")