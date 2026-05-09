import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
npm = r'C:\Program Files\nodejs\npm.cmd'
print("🔨 开始编译...")
build_res = subprocess.run([npm, 'run', 'build'], cwd=base_dir, capture_output=True, text=True)
print(f"Build return code: {build_res.returncode}")
if build_res.returncode == 0:
    print("\n🎉 编译成功！老板您领导有方！👏")
    print(f"\n{build_res.stdout}")
    dist_path = os.path.join(base_dir, 'dist')
    if os.path.exists(dist_path):
        files = os.listdir(dist_path)
        print(f"\n📂 编译产物目录：{dist_path}")
        print(f"📋 文件：{files}")
        # 统计文件大小
        total_size = 0
        for f in files:
            fp = os.path.join(dist_path, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
        print(f"📊 总大小：{round(total_size / 1024 / 1024, 2)} MB")
else:
    print("\n❌ 编译失败：")
    print(build_res.stderr)