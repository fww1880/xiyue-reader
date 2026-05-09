import os, sys, subprocess, time
import psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
# 关闭旧进程
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
    except: pass
time.sleep(1.5)
# 启动新进程
print("🚀 重启「喜阅」（关于页面更新版）...")
process = subprocess.Popen(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)
if process.poll() is None:
    print(f"✅ 喜阅启动成功！PID: {process.pid}")
else:
    print("❌ 启动失败")
print("\n💡 现在点击菜单栏的「帮助」→「关于」，就能看到：")
print("  📖 木木和叶子的喜阅")
print("  © 2026 木木和叶子")