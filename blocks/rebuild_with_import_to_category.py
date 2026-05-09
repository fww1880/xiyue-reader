import os, sys, subprocess, shutil, psutil, time
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
# 杀掉旧进程
print("🔪 杀掉所有运行中的喜阅进程...")
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if '喜阅.exe' in proc.info.get('name', ''):
            proc.kill()
            proc.wait()
    except: pass
time.sleep(2)
# 清理旧构建
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧 build 目录")
# 打包
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
print("\n🚀 开始打包（右键导入书籍到指定分类版本）...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"\n✨ 新功能：右键导入书籍到指定分类")
        print(f"  - 右键空白处：📂 导入书籍文件 / 📚 导入书籍文件夹")
        print(f"  - 右键分类名：📂 导入书籍到本分类 / 📚 导入文件夹到本分类")
        print(f"  - 右键书籍名：🗑️ 删除本书")
else:
    print(f"\n❌ 打包失败：\n{res.stderr}")