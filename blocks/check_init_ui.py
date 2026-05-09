import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
print("🔍 检查 init_ui 方法：")
in_method = False
for i, line in enumerate(lines, 1):
    if 'def init_ui(self):' in line:
        in_method = True
        print(f"L{i}: {line.strip()}")
        continue
    if in_method:
        print(f"L{i}: {line.strip()}")
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            break