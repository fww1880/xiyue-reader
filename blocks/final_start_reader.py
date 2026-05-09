import os, sys, subprocess, time
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 清理
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
            print(f"🧹 清理旧进程 PID: {proc.info['pid']}")
    except: pass
time.sleep(1.5)
# 启动
print("🚀 最终启动阅读器...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2.5)
found = False
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器成功启动并运行！PID: {proc.info['pid']}")
            found = True
            break
    except: pass
if not found:
    print("❌ 未找到运行进程，可能还是有问题")
else:
    print("\n🎉 一切就绪！老板可以正常使用了！")