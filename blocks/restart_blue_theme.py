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
print("🚀 启动「喜阅」（蓝色清爽版）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎨 蓝色清爽界面说明：")
print("  1️⃣ 工具栏 → 浅蓝渐变背景，按钮无边框，按下变深蓝")
print("  2️⃣ 书架面板 → 淡蓝背景，蓝色标题栏，无边框")
print("  3️⃣ 正文区域 → 纯白/浅灰底色，完全无边框")
print("  4️⃣ 窗口阴影 → 淡蓝色柔和阴影，告别黑边黑框")