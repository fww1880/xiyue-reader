import os
import subprocess
import sys
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
spec_file = os.path.join(novel_reader_dir, 'main.spec')
# 清理旧的构建文件
import shutil
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print("🧹 已清理旧的 dist 目录")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("🧹 已清理旧的 build 目录")
if os.path.exists(spec_file):
    os.remove(spec_file)
    print("🧹 已清理旧的 spec 文件")
# 构建 PyInstaller 命令
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",           # 单个文件
    "--windowed",          # 无控制台窗口
    f"--icon={icon_path}", # 使用卡通书本图标
    "--name=喜阅",         # 输出文件名
    "--add-data=assets;assets" if os.path.exists(os.path.join(novel_reader_dir, 'assets')) else "",
    main_file
]
# 过滤空参数
cmd = [c for c in cmd if c]
print(f"🚀 开始打包：{' '.join(cmd)}")
try:
    result = subprocess.run(
        cmd,
        cwd=novel_reader_dir,
        capture_output=True,
        text=True,
        timeout=300  # 5 分钟超时
    )
    if result.returncode == 0:
        exe_path = os.path.join(dist_dir, '喜阅.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"✅ 打包成功！")
            print(f"📦 可执行文件位置：{exe_path}")
            print(f"📊 文件大小：{file_size:.2f} MB")
            print(f"🎨 已应用卡通书本图标：{icon_path}")
        else:
            print("❌ 打包完成但未找到生成的 exe 文件")
    else:
        print(f"❌ 打包失败，错误代码：{result.returncode}")
        print(f"错误信息：{result.stderr}")
except subprocess.TimeoutExpired:
    print("⏰ 打包超时（超过 5 分钟）")
except Exception as e:
    print(f"❌ 打包过程出错：{str(e)}")