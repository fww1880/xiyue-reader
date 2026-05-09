import os, sys, subprocess, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
print("🔧 正在修复 main.py 语法错误...")
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复多余的括号
content = content.replace("self.setWindowIcon(QIcon(resource_path('book_icon.ico'))))", "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))")
print("✅ 语法错误已修复")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("📦 开始重新打包...")
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
if os.path.exists(dist_dir): shutil.rmtree(dist_dir)
if os.path.exists(build_dir): shutil.rmtree(build_dir)
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"🎨 窗口标题：喜阅")
        print(f"🎨 窗口图标：卡通书本（已深度嵌入）")
    else:
        print("❌ 打包完成但未找到 exe 文件")
else:
    print(f"❌ 打包失败：{res.stderr}")