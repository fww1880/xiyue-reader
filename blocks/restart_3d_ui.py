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
print("🚀 启动「喜阅」（立体界面版）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎨 立体界面效果说明：")
print("  1️⃣ 工具栏 → 渐变背景 + 凸起按钮 + 按下凹陷")
print("  2️⃣ 书架面板 → 渐变边框 + 圆角 + 立体标题栏")
print("  3️⃣ 正文区域 → 内嵌式边框 + 柔和渐变背景")
print("  4️⃣ 主窗口 → 外部阴影，悬浮感")