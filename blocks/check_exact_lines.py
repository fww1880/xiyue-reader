import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 L1175-L1195 精确内容：")
for i in range(1174, min(1196, len(lines))):
    print(f"  L{i+1}: {repr(lines[i])}")