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
print("\n🚀 开始打包（修复添加书签闪退 - 缺失函数问题）...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"\n🔧 本次修复内容：")
        print(f"  1. ✅ 添加了缺失的 add_bookmark 函数（之前代码中根本没有这个函数！）")
        print(f"  2. ✅ 添加了 get_position_preview 函数")
        print(f"  3. ✅ 两个函数都包含完整的 try-except 错误处理")
        print(f"  4. ✅ 添加了 current_book_path 和 text_edit 存在性检查")
        print(f"\n💡 闪退根本原因：")
        print(f"  工具栏和右键菜单都连接了 self.add_bookmark，但这个函数从未定义！")
        print(f"  点击按钮时调用不存在的函数 → AttributeError → 闪退")
else:
    print(f"\n❌ 打包失败：\n{res.stderr}")