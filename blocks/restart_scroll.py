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
print("🚀 启动阅读器（滚屏功能已优化）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎯 滚屏功能升级内容：")
print("  1️⃣ 📜 滚屏按钮 → 点击开启，文字变为「⏸️ 暂停」，再点暂停")
print("  2️⃣ ⌨️ 快捷键 → Ctrl+Space 快速开关滚屏")
print("  3️⃣ 🐢 减速 / 🐇 加速 → 实时调节滚屏速度")
print("  4️⃣ 🏁 自动停止 → 滚到底部自动结束")
print("  5️⃣ 📊 状态栏提示 → 实时显示滚屏状态和速度")