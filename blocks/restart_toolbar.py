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
print("🚀 启动阅读器（工具栏样式已优化）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎯 本次优化内容：")
print("  1️⃣ 图标缩小 → 从 28×28 → 22×22，工具栏更紧凑")
print("  2️⃣ 立体效果 → 按钮增加边框、圆角、悬停变色、按下凹陷效果")
print("  3️⃣ 按下弹起 → 点击时有真实的物理凹陷感，反馈更清晰")