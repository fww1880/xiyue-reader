import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找窗口初始化和大小设置相关代码
import re
# 查找 __init__ 方法或者 setup_ui 方法中的相关设置
matches = re.findall(r'(def __init__|def setup_ui|setMinimumSize|setMaximumSize|setFixedSize|resize).*?(?=def \w+\(|\Z)', content, re.DOTALL)
print("找到相关代码块：")
for i, m in enumerate(matches):
    print(f"--- Block {i+1} ---")
    print(m[:500]) # 打印前500字符
    if len(m) > 500: print("...")