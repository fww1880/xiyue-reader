import os, sys, subprocess, time
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 清理旧进程
print("🧹 清理旧进程...")
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
    except: pass
time.sleep(1.5)
# 启动
print("🚀 重新启动阅读器...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
found = False
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器已启动！PID: {proc.info['pid']}")
            found = True
            break
    except: pass
if not found:
    print("⚠️ 未检测到进程，请检查是否有报错弹窗。")