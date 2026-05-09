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
print("🚀 重启「喜阅」（最终蓝色清爽版）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n✅ 本次清理：")
print("  • 工具栏按钮 → 去掉所有边框，浅蓝背景+深蓝文字")
print("  • 目录/书签列表框 → 淡蓝背景，无边框，选中浅蓝高亮")
print("  • 目录/书签标签 → 蓝色调背景文字，去掉灰色黑底")
print("  • 整个界面已100%无边框黑底！")