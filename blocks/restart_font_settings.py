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
print("🚀 启动阅读器（字体设置已升级）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎯 本次升级内容：")
print("  1️⃣ 默认字号 → 从 16 改为 18")
print("  2️⃣ 新增字体选择 → 下拉框选择系统所有字体")
print("  3️⃣ 新增粗细选择 → 正常/粗体二选一")
print("  4️⃣ 字号范围扩大 → 8-48（之前是 8-36）")
print("  5️⃣ 所有设置自动保存，重启后保持")