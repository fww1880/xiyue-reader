import os
import sys
import subprocess
# 杀掉旧进程
print("🔄 关闭旧进程...")
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'main.py' in ' '.join(cmdline) and 'novel_reader' in ' '.join(cmdline):
                proc.kill()
                print(f"  ✅ 已关闭旧进程 PID: {proc.info['pid']}")
        except:
            pass
except:
    pass
# 启动阅读器
print("\n🚀 启动阅读器...")
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
try:
    process = subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ 阅读器已启动！请查看桌面窗口。")
    print("\n💡 提示：")
    print("- 书架窗口可以拖动、调整大小")
    print("- 按 Ctrl+B 可以快速显示/隐藏书架")
    print("- 可以把书架拖出来成为独立窗口")
except Exception as e:
    print(f"❌ 启动失败：{e}")