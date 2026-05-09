import os, sys, subprocess, time
import psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
# 先关闭所有旧进程
closed_count = 0
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])) or '喜阅.exe' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
            closed_count += 1
    except:
        pass
print(f"🔌 已关闭 {closed_count} 个旧进程")
time.sleep(1.5)
# 重新启动
print("🚀 重新打开「喜阅」...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅已重新打开！PID: {proc.info['pid']}")
            break
    except: pass
print("\n💡 现在重新打开后，应该会自动恢复上次关闭前的所有状态：")
print("  • 如果上次打开过书，会自动打开并回到阅读进度")
print("  • 字体、主题、窗口大小位置都保持原样")
print("  • 书签都在，书架状态不变")