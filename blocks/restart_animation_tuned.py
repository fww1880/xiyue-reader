import os, sys, subprocess, time
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 关闭旧进程
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
    except: pass
time.sleep(1.5)
# 启动新进程
print("🚀 启动阅读器（翻页动画已调慢调明显）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎯 本次调整：")
print("  1️⃣ 动画时长 → 从 300ms → 400ms，动画更慢更清晰")
print("  2️⃣ 缓动曲线 → 从 OutCubic → OutQuad，动画效果更明显")
print("  3️⃣ 所有6个翻页方法都已正确添加动画")
print("  4️⃣ 工具栏按钮绑定正确")