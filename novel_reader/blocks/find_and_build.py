import subprocess, sys, os
# 先查看当前工作目录
current_dir = os.getcwd()
print(f"📂 当前工作目录：{current_dir}")
print(f"📂 目录内容：{os.listdir(current_dir)[:20]}")
# 查找 novel_reader 目录
possible_paths = [
    os.path.join(current_dir, 'novel_reader'),
    os.path.join(os.path.dirname(current_dir), 'novel_reader'),
    r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader',
]
novel_reader_dir = None
for p in possible_paths:
    if os.path.exists(p) and os.path.isdir(p):
        novel_reader_dir = p
        print(f"✅ 找到 novel_reader 目录：{novel_reader_dir}")
        break
if novel_reader_dir is None:
    print("⚠️ 未找到 novel_reader 目录，搜索上级目录...")
    for root, dirs, files in os.walk(current_dir):
        if 'novel_reader' in dirs:
            novel_reader_dir = os.path.join(root, 'novel_reader')
            print(f"✅ 找到：{novel_reader_dir}")
            break
if novel_reader_dir:
    os.chdir(novel_reader_dir)
    print(f"📂 当前目录内容：{os.listdir('.')[:30]}")
    icon_file = os.path.join(novel_reader_dir, 'icon.svg')
    print("\n📦 开始打包「喜阅」为可执行文件...")
    print("   正在打包，请稍候（约 1-2 分钟）...\n")
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
    if os.path.exists(icon_file):
        cmd.append(f'--icon={icon_file}')
        cmd.append(f'--add-data={icon_file};.')
        print(f"✅ 包含图标：{icon_file}")
    cmd.append("main.py")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.stdout:
        print(result.stdout[-2000:])
    if result.returncode == 0:
        print("\n✅ 打包成功！")
    else:
        print(f"\n❌ 打包失败：")
        print(result.stderr[-1500:])