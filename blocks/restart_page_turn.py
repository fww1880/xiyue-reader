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
print("🚀 启动阅读器（翻页动画已添加）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎯 本次新增功能：")
print("  1️⃣ 点击 ⬅️ 上页 / ➡️ 下页 → 页面平滑滚动，模拟翻页效果")
print("  2️⃣ 键盘 PageUp/PageDown → 同样有平滑动画")
print("  3️⃣ 动画参数：300ms 时长 + OutCubic 缓动曲线，先快后慢")