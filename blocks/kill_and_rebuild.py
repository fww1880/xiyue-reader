import os, sys, subprocess, shutil, psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
print("🔪 正在杀掉运行中的喜阅进程...")
# 杀掉所有喜阅.exe 进程
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if proc.info['name'] == '喜阅.exe':
            print(f"  杀掉进程 PID {proc.info['pid']}")
            proc.kill()
            proc.wait()
    except Exception as e:
        print(f"  杀进程失败：{e}")
# 等待一会儿
import time
time.sleep(2)
# 尝试删除 dist 目录
if os.path.exists(dist_dir):
    try:
        shutil.rmtree(dist_dir)
        print("🧹 已删除旧的 dist 目录")
    except Exception as e:
        print(f"⚠️ 删除 dist 目录失败：{e}，继续打包...")
if os.path.exists(build_dir):
    try:
        shutil.rmtree(build_dir)
        print("🧹 已删除旧的 build 目录")
    except Exception as e:
        print(f"⚠️ 删除 build 目录失败：{e}")
# 重新打包
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
print("\n🚀 开始重新打包...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"🔧 修复：resource_path() 关键字参数调用错误")
    else:
        print("\n❌ 打包完成但未找到 exe 文件")
else:
    print(f"\n❌ 打包失败：{res.stderr}")