import subprocess, sys, os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
os.chdir(novel_reader_dir)
print("📦 打包「喜阅」为可执行文件（无图标）...")
print("   正在打包，请稍候（约 2-3 分钟）...\n")
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "喜阅",
    "--distpath", os.path.join(novel_reader_dir, "dist"),
    "--workpath", os.path.join(novel_reader_dir, "build"),
    "--specpath", novel_reader_dir,
    "--clean",
    "--noconfirm",
    "main.py"
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
if result.stdout:
    # 只显示最后部分
    lines = result.stdout.split('\n')
    for line in lines[-20:]:
        if line.strip():
            print(f"  {line.strip()}")
if result.returncode == 0:
    print("\n✅ 打包成功！")
else:
    print(f"\n❌ 打包失败：")
    for line in result.stderr.split('\n')[-10:]:
        if line.strip():
            print(f"  {line.strip()}")