import subprocess, sys, os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_file = os.path.join(novel_reader_dir, 'icon.svg')
# 切换到 novel_reader 目录
os.chdir(novel_reader_dir)
print("📦 开始打包「喜阅」为可执行文件...")
print("   正在打包，请稍候（约 1-2 分钟）...\n")
# 构建 PyInstaller 命令
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
]
# 如果有图标，用正确的语法添加
if os.path.exists(icon_file):
    cmd.append(f'--icon={icon_file}')
    cmd.append(f'--add-data={icon_file};.')
    print(f"✅ 包含图标文件：{icon_file}")
cmd.append("main.py")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
print(result.stdout[-2000:] if result.stdout else "")
if result.returncode == 0:
    print("\n✅ 打包成功！")
else:
    # 打印更详细的错误
    print(f"\n❌ 打包失败，错误信息：")
    print(result.stderr[-1000:])