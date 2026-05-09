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
print("🚀 重启「喜阅」（测试自动保存/恢复功能）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n💾 自动保存功能说明：")
print("  ✅ 关闭时自动保存：")
print("    • 当前打开的书籍路径")
print("    • 阅读进度（光标位置）")
print("    • 字体设置（字体、字号、粗细、行高）")
print("    • 主题模式（白天/夜间/护眼）")
print("    • 窗口大小和位置")
print("    • 书架面板状态（浮动/固定、显示/隐藏）")
print("    • 所有书签（实时保存 + 关闭时确保）")
print("\n  🔄 下次启动时自动恢复以上所有状态！")