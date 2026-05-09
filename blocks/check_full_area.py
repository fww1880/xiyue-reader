import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("行号: 内容 (开头空格数)")
print("-" * 60)
for i in range(1000, min(1120, len(lines))):
    line = lines[i]
    leading_spaces = len(line) - len(line.lstrip())
    print(f"L{i+1:4d}: {' ' * leading_spaces}{line.strip()} (leading: {leading_spaces})")
print("=" * 60)