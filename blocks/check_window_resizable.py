import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找窗口大小设置相关代码
import re
matches = re.findall(r'.{0,50}(setFixedSize|setMinimumSize|setMaximumSize|setSizePolicy|resize|setGeometry|QMainWindow|QWidget).{0,50}', content)
print("找到相关设置：")
for m in matches:
    print(m)