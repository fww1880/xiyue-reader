import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 create_tool_bar 开始位置
start_line = None
for i, line in enumerate(lines):
    if 'def create_tool_bar(self):' in line:
        start_line = i
        break
if start_line is not None:
    # 读取到下一个 def 结束
    for i in range(start_line, len(lines)):
        if i > start_line + 200:
            break
        print(f"{i+1}: {lines[i].rstrip()}")
        # 检测下一个方法定义
        if i > start_line + 10 and lines[i].strip().startswith('def '):
            break