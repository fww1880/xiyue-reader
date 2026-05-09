import os, sys, subprocess, shutil, psutil, time
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
# 1. 修改代码：注释掉最小尺寸限制，实现“随意”调整大小
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 替换掉之前修改的 400, 300 或者直接注释掉
if 'self.setMinimumSize(400, 300)' in content:
    content = content.replace('self.setMinimumSize(400, 300)', '# self.setMinimumSize(400, 300) # 已注释，允许随意调整大小')
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已移除窗口最小尺寸限制，现在可以随意拖动边框调整大小！")
elif 'self.setMinimumSize(1200, 800)' in content:
    content = content.replace('self.setMinimumSize(1200, 800)', '# self.setMinimumSize(1200, 800) # 已注释，允许随意调整大小')
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已移除窗口最小尺寸限制（原1200x800），现在可以随意拖动边框调整大小！")
else:
    print("⚠️ 未找到 setMinimumSize，可能已经被移除或修改。")
# 2. 杀掉旧进程
print("🔪 杀掉所有运行中的喜阅进程...")
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if '喜阅.exe' in proc.info.get('name', ''):
            proc.kill()
            proc.wait()
    except: pass
time.sleep(2)
# 3. 清理旧构建
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧 build 目录")
# 4. 打包
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
print("\n🚀 开始打包...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
else:
    print(f"\n❌ 打包失败：\n{res.stderr}")