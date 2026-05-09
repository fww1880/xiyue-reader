import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔍 查找所有 package.json 文件...")
found = []
for root, dirs, files in os.walk(base_dir):
    if 'node_modules' in root or '.git' in root:
        continue
    if 'package.json' in files:
        pj_path = os.path.join(root, 'package.json')
        found.append(pj_path)
        print(f"✅ 找到：{pj_path}")
if not found:
    print("❌ 没有找到 package.json！需要我帮您重新创建一个正确的 package.json！")