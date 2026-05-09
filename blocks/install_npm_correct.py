import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
npm = r'C:\Program Files\nodejs\npm.cmd'
print(f"📂 项目根目录：{base_dir}")
print(f"🔍 检查 package.json 是否存在：{os.path.exists(os.path.join(base_dir, 'package.json'))}")
print(f"🔍 检查 novel_reader 目录：{os.path.exists(os.path.join(base_dir, 'novel_reader'))}")
# 列出 novel_reader 目录内容
novel_reader_dir = os.path.join(base_dir, 'novel_reader')
print(f"\n📋 novel_reader 目录内容：")
for entry in os.scandir(novel_reader_dir):
    print(f"  {'📁' if entry.is_dir() else '📄'} {entry.name}")
# 检查根目录 package.json 内容
with open(os.path.join(base_dir, 'package.json'), 'r', encoding='utf-8') as f:
    import json
    pkg = json.load(f)
    print(f"\n📦 name: {pkg.get('name')}, version: {pkg.get('version')}")
    print(f"🔨 scripts: {list(pkg.get('scripts', {}).keys())}")
print("\n📦 开始安装依赖...")
res = subprocess.run([npm, 'install'], cwd=base_dir, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if res.returncode != 0:
    print("\n=== stderr ===")
    print(res.stderr)
else:
    print("\n✅ 依赖安装完成！")