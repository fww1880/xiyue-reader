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
print("🚀 重启「喜阅」（修复标题显示+自动换行）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n✅ 修改内容：")
print("  1. 书架标题栏：增加上下内边距（10px → 12px），\"我的书架\"完整显示不裁切")
print("  2. 正文区域：启用自动换行 → `WidgetWidth`模式，拖动改变大小时自动换行适应")
print("  3. 书架边框：QyQt Dock默认支持自由拖动改变大小，无需修改直接可用")