import os, sys, subprocess
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 关闭旧进程
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        cl = proc.info.get('cmdline', [])
        if cl and 'main.py' in ' '.join(cl) and 'novel_reader' in ' '.join(cl):
            proc.kill()
            print(f"✅ 已关闭旧进程 {proc.info['pid']}")
    except:
        pass
# 启动
print("🚀 重新启动阅读器...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
print("✅ 阅读器已重启，右键菜单+点击跳转功能已生效！")