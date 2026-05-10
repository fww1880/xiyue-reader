import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("📋 检查本地项目结构...")
# 检查 buildozer.spec 文件是否存在
spec_path = os.path.join(base_dir, 'buildozer.spec')
if os.path.exists(spec_path):
    print(f"✅ 找到 buildozer.spec 文件")
    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"内容预览（前200字符）：")
        print(content[:200])
else:
    print(f"❌ 没有 buildozer.spec 文件！")
    print("这是关键问题！Buildozer 需要一个配置文件才能打包！")
# 检查项目目录结构
print(f"\n📁 项目目录结构：")
for item in os.listdir(base_dir):
    if os.path.isdir(os.path.join(base_dir, item)):
        print(f"  📂 {item}")
    else:
        print(f"  📄 {item}")