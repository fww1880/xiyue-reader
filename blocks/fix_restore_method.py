import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
# 查找所有 def 方法名，看看打开书籍的方法叫什么
print("🔍 查找所有方法定义：")
for i, line in enumerate(lines, 1):
    if 'def ' in line and 'self' in line:
        method_name = line.strip().split('(')[0].replace('def ', '').strip()
        print(f"  L{i}: {method_name}")