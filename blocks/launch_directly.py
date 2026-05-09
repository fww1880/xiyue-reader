import os, sys, subprocess, time
import psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
# 关闭旧进程
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
            print(f"🔌 已关闭旧进程 PID: {proc.info['pid']}")
    except: pass
time.sleep(1.5)
# 直接后台启动（不等待输出）
print("🚀 启动「喜阅」...")
process = subprocess.Popen(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)
# 检查是否在运行
if process.poll() is None:
    print(f"✅ 喜阅已成功打开！PID: {process.pid}")
else:
    print("❌ 进程启动后退出，可能有错误")
    # 重新运行一次捕获错误
    result = subprocess.run([sys.executable, main_file], cwd=novel_reader_dir, capture_output=True, text=True, timeout=5)
    if result.stderr:
        print(f"📝 错误信息：{result.stderr[-500:]}")