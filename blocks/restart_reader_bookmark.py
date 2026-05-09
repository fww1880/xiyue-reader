import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 杀旧进程
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cl = proc.info.get('cmdline', [])
            if cl and 'main.py' in ' '.join(cl) and 'novel_reader' in ' '.join(cl):
                proc.kill()
                print(f"✅ 已关闭旧进程 {proc.info['pid']}")
        except: pass
except: pass
# 启动
print("🚀 启动阅读器...")
try:
    subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ 阅读器已启动！书签功能已上线。")
except Exception as e:
    print(f"❌ 失败：{e}")