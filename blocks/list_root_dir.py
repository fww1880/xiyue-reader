import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print(f"📂 列出根目录文件：{base_dir}")
for entry in os.scandir(base_dir):
    if entry.is_dir():
        print(f"  📁 {entry.name}")
    else:
        print(f"  📄 {entry.name}")