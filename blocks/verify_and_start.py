import os, sys, subprocess, time
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 语法检查
result = subprocess.run(
    [sys.executable, '-m', 'py_compile', main_file],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ 语法检查通过")
else:
    print("❌ 语法错误：")
    print(result.stderr)
    exit()
# 清理
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
    except: pass
time.sleep(1.5)
# 启动
print("🚀 启动阅读器...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
found = False
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 阅读器启动成功！PID: {proc.info['pid']}")
            found = True
            break
    except: pass
if not found:
    print("❌ 未找到运行进程")
else:
    print("\n🎉 现在书架面板的书签栏应该正常展示了！")