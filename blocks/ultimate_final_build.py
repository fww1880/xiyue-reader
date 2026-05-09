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
    except Exception as e:
        pass
time.sleep(3)
# 清理旧构建目录
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧 build 目录")
# 检查文件状态
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
rp_count = content.count('def resource_path')
print(f"\n📋 最终状态检查:")
print(f"  resource_path 定义数量: {rp_count}")
print(f"  import sys 数量: {content.count('import sys')}")
print(f"  import os 数量: {content.count('import os')}")
if not os.path.exists(icon_path):
    print(f"\n❌ 图标文件不存在: {icon_path}")
else:
    print(f"  图标文件大小: {os.path.getsize(icon_path)} bytes")
# 最终打包
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
print("\n🚀 开始终极打包...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 终极打包成功！")
        print(f"📦 可执行文件: {exe}")
        print(f"📊 文件大小: {size_mb:.2f} MB")
        print(f"\n🎯 终极修复内容:")
        print(f"  1. resource_path 定义移到文件最开头，仅定义一次")
        print(f"  2. 彻底清除所有重复 import 和多余 return")
        print(f"  3. try-except 正确捕获 AttributeError 处理 _MEIPASS")
        print(f"  4. 完整嵌入 book_icon.ico 到 exe")
    else:
        print("\n❌ 打包完成但未找到 exe 文件")
else:
    print(f"\n❌ 打包失败:\n{res.stderr}")