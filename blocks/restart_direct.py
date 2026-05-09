import os
import sys
import subprocess
import psutil
# 杀死所有Python进程
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if 'python' in proc.info['name'].lower():
            proc.kill()
    except:
        pass
print("🔄 已关闭旧进程，准备启动新阅读器...")
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
if not os.path.exists(main_file):
    print(f"❌ 找不到主程序: {main_file}")
else:
    print(f"✅ 找到主程序: {main_file}")
    # 直接启动，不改变当前工作目录
    subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("🚀 小说阅读器启动成功！请检查窗口是否弹出。")