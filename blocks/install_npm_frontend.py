import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel-reader-frontend'
npm = r'C:\Program Files\nodejs\npm.cmd'
print(f"📂 工作目录：{base_dir}")
print(f"🔧 使用 npm：{npm}")
# 查看目录下文件
files = os.listdir(base_dir)
print(f"\n📋 目录文件：{files}")
print("\n📦 安装依赖...")
res = subprocess.run([npm, 'install'], cwd=base_dir, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if res.returncode == 0:
    print("\n✅ 依赖安装成功！")
else:
    print("\n=== stdout ===")
    print(res.stdout)
    print("\n=== stderr ===")
    print(res.stderr)