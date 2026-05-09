import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
npm = r'C:\Program Files\nodejs\npm.cmd'
print("📦 重新安装依赖，捕获完整输出...")
res = subprocess.run([npm, 'install'], cwd=base_dir, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
print("\n=== stdout ===")
print(res.stdout)
print("\n=== stderr ===")
print(res.stderr)