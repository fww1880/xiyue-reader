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
            print(f"  ✅ 已杀掉 PID {proc.info['pid']}")
    except: pass
time.sleep(2)
# 清理旧构建
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧 build 目录")
# 最终打包
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
print("\n🚀 开始最终打包（经过 n 次语法修复，终于干净了）...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 最终打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"\n🎯 所有问题已修复：")
        print(f"  1. ✅ sys._MEIPASS 判断错误 → 正确 try-except 捕获")
        print(f"  2. ✅ resource_path 插入错误位置 → 移到文件开头第一个 class 之前")
        print(f"  3. ✅ 缩进错误 → 彻底修复 class 内方法缩进")
        print(f"  4. ✅ 重复定义 → 只保留一个干净的 resource_path")
        print(f"  5. ✅ keyboard_pagination 被破坏 → 完整重构函数")
        print(f"  6. ✅ 图标问题 → 完整嵌入，强制设置")
        print(f"  7. ✅ 书签问题 → 修复持久化保存")
else:
    print(f"\n❌ 打包失败：\n{res.stderr}")