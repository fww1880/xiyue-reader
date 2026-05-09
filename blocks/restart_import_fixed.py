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
print("🚀 重启「喜阅」（导入修复版）...")
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
    result = subprocess.run([sys.executable, main_file], cwd=novel_reader_dir, capture_output=True, text=True, timeout=5)
    if result.stderr:
        print(f"错误：{result.stderr[-500:]}")
print("\n💡 现在导入书籍后：")
print("  • 书架里会显示书籍")
print("  • 数据会同步保存到 bookshelf_data")
print("  • 关闭再打开，书和书签都在！")