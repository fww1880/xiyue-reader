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
print("🚀 重启「喜阅」（恢复白天/夜间/护眼模式）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎨 阅读模式说明：")
print("  ☀️ 白天模式 → 纯白背景 + 黑色文字（经典阅读）")
print("  🌙 夜间模式 → 深色背景 + 浅灰文字（护眼不刺眼）")
print("  🌿 护眼模式 → 豆沙绿背景 + 黑色文字（柔和舒适）")
print("\n💡 工具栏已保留蓝色清爽风格，点击三个按钮即可切换阅读背景！")