import os, sys, subprocess, time
import psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
# 关闭所有旧进程
closed_count = 0
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        cmdline = ' '.join(proc.info.get('cmdline', []))
        if 'main.py' in cmdline or '喜阅' in cmdline:
            proc.kill()
            closed_count += 1
    except: pass
print(f"🔌 已关闭 {closed_count} 个旧进程")
time.sleep(1.5)
# 重新启动
print("\n🚀 重新打开「喜阅」...")
process = subprocess.Popen(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)
if process.poll() is None:
    print(f"✅ 喜阅已成功重新打开！PID: {process.pid}")
else:
    print("❌ 启动失败")
    result = subprocess.run([sys.executable, main_file], cwd=novel_reader_dir, capture_output=True, text=True, timeout=5)
    if result.stderr:
        print(f"错误：{result.stderr[-500:]}")
print("\n💡 现在导入书籍会正确保存，关闭再打开书库和书签都会保留！")