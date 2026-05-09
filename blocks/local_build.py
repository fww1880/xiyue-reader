import subprocess, os, shutil
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔧 清除代理配置...")
subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)
print("\n📦 安装依赖（uv）...")
res = subprocess.run(['uv', 'run', 'pnpm', 'install'], cwd=base_dir, capture_output=False, text=True)
# 如果 uv pnpm 不行，试试 pnpm
if res.returncode != 0:
    print("\n⚠️ uv pnpm 失败，直接尝试 pnpm...")
    res = subprocess.run(['pnpm', 'install'], cwd=base_dir, capture_output=False, text=True)
if res.returncode != 0:
    print("\n⚠️ pnpm 失败，试试 npm...")
    res = subprocess.run(['npm', 'install'], cwd=base_dir, capture_output=False, text=True)
if res.returncode == 0:
    print("\n✅ 依赖安装完成！开始编译...")
    build_res = subprocess.run(['pnpm', 'run', 'build'], cwd=base_dir, capture_output=True, text=True)
    if build_res.returncode == 0:
        print("\n🎉 编译成功！")
        dist_path = os.path.join(base_dir, 'dist')
        print(f"\n📂 产物目录：{dist_path}")
        files = os.listdir(dist_path)
        print(f"📋 文件列表：{files}")
    else:
        print(f"\n❌ 编译失败：\n{build_res.stderr}")
else:
    print("\n❌ 依赖安装失败，请检查环境配置！")