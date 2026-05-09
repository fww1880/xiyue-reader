import os
import subprocess
import sys
import shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
# 清理旧的构建文件
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧的 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧的 build 目录")
# 构建 PyInstaller 命令
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    f"--icon={icon_path}",
    "--name=喜阅",
    main_file
]
print(f"🚀 开始重新打包...")
result = subprocess.run(
    cmd,
    cwd=novel_reader_dir,
    capture_output=True,
    text=True,
    timeout=300
)
if result.returncode == 0:
    exe_path = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✅ 重新打包成功！")
        print(f"📦 位置：{exe_path}")
        print(f"📊 大小：{file_size:.2f} MB")
        print(f"🎨 窗口标题：喜阅")
        print(f"🎨 窗口图标：卡通书本（book_icon.ico）")
    else:
        print("❌ 未找到生成的 exe 文件")
else:
    print(f"❌ 打包失败：{result.stderr}")