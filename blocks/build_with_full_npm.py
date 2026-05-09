import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
npm = r'C:\Program Files\nodejs\npm.cmd'
print(f"🔧 使用 npm：{npm}")
print("\n📦 安装依赖...")
res = subprocess.run([npm, 'install'], cwd=base_dir, capture_output=False, text=True)
if res.returncode == 0:
    print("\n✅ 依赖安装完成！开始编译...")
    # 编译命令是 npm run build
    build_res = subprocess.run([npm, 'run', 'build'], cwd=base_dir, capture_output=True, text=True)
    if build_res.returncode == 0:
        print("\n🎉 编译成功！")
        print(f"\n{build_res.stdout}")
        dist_path = os.path.join(base_dir, 'dist')
        if os.path.exists(dist_path):
            files = os.listdir(dist_path)
            print(f"\n📂 产物目录：{dist_path}")
            print(f"📋 编译产物：{files}")
        else:
            print(f"\n⚠️ dist 目录不存在，编译可能有问题")
    else:
        print(f"\n❌ 编译失败：\n{build_res.stderr}")
else:
    print("\n❌ 依赖安装失败！")