import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
npm = r'C:\Program Files\nodejs\npm.cmd'
print("📦 安装依赖...")
res = subprocess.run([npm, 'install'], cwd=base_dir, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if res.returncode != 0:
    print("\n=== stdout ===")
    print(res.stdout)
    print("\n=== stderr ===")
    print(res.stderr)
else:
    print("\n✅ 依赖安装成功！")
    print("\n🔨 开始编译...")
    build_res = subprocess.run([npm, 'run', 'build'], cwd=base_dir, capture_output=True, text=True)
    print(f"Build return code: {build_res.returncode}")
    if build_res.returncode == 0:
        print("\n🎉 编译成功！")
        print(f"\n{build_res.stdout}")
        dist_path = os.path.join(base_dir, 'dist')
        if os.path.exists(dist_path):
            files = os.listdir(dist_path)
            print(f"\n📂 产物目录：{dist_path}")
            print(f"📋 编译产物：{files}")
        else:
            print(f"\n⚠️ dist 目录不存在，看看在哪里...")
            # 查找 dist 目录
            for root, dirs, files in os.walk(base_dir):
                if 'dist' in dirs:
                    print(f"✅ 找到 dist：{os.path.join(root, 'dist')}")
    else:
        print("\n❌ 编译失败：")
        print(build_res.stderr)