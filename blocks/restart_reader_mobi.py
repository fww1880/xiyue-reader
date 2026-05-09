import os
import sys
import subprocess
# 杀掉旧进程，启动新进程
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
print("\n🚀 启动阅读器...")
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
try:
    process = subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ 阅读器已启动！请查看桌面窗口。")
    print("\n💡 提示：请打开一本MOBI文件测试目录是否显示")
except Exception as e:
    print(f"❌ 启动失败：{e}")