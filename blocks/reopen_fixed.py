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
# 先测试运行看有没有报错
print("🔍 测试运行检查报错...")
result = subprocess.run([sys.executable, main_file], cwd=novel_reader_dir, capture_output=True, text=True, timeout=3)
if result.stderr:
    print(f"❌ 仍有错误：{result.stderr[-500:]}")
else:
    print("✅ 无报错，启动成功！")
    # 用 Popen 后台启动
    subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    time.sleep(1.5)
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
                print(f"✅ 喜阅已成功打开！PID: {proc.info['pid']}")
                break
        except: pass