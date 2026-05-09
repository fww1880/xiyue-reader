import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔍 查找 index.html...")
found = []
for root, dirs, files in os.walk(base_dir):
    if 'node_modules' in root or '.git' in root or 'dist' in root:
        continue
    if 'index.html' in files:
        found.append(os.path.join(root, 'index.html'))
        print(f"✅ 找到：{os.path.join(root, 'index.html')}")
if not found:
    print("❌ 没找到 index.html！让我看看 src 目录...")
for root, dirs, files in os.walk(base_dir):
    if 'node_modules' in root or '.git' in root:
        continue
    if 'src' in dirs:
        print(f"📁 找到 src 目录：{os.path.join(root, 'src')}")
        src_files = os.listdir(os.path.join(root, 'src'))
        print(f"   src 文件：{src_files}")