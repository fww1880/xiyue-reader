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
print("🚀 重启「喜阅」（验证主题切换）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎨 现在的切换逻辑：")
print("  ☀️ 点击“白天” → 纯白底 (#FFFFFF) + 黑字")
print("  🌙 点击“夜间” → 深黑底 (#1A1A1A) + 浅灰字")
print("  🌿 点击“护眼” → 豆沙绿底 (#CCE8CF) + 黑字")
print("\n💡 已使用 setStyleSheet 强制生效，确保所见即所得！")