import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print("🚀 打开阅读器...")
try:
    subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ 阅读器已启动！")
except Exception as e:
    print(f"❌ 启动失败：{e}")