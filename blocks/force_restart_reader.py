import os, sys, subprocess, time
import psutil
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 1. 彻底清理旧进程
print("🧹 正在清理所有旧进程...")
killed = False
for proc in psutil.process_iter(['pid', 'cmdline', 'name']):
    try:
        cl = proc.info.get('cmdline', [])
        if cl and 'main.py' in ' '.join(cl):
            print(f"  -> 终止进程 {proc.info['pid']}")
            proc.kill()
            killed = True
    except: pass
if killed:
    time.sleep(1.5)
else:
    print("  -> 未发现残留进程")
# 2. 检查文件
if not os.path.exists(main_file):
    print(f"❌ 错误：找不到启动文件 {main_file}")
else:
    print(f"✅ 启动文件就绪")
# 3. 启动阅读器
print("🚀 正在启动阅读器...")
try:
    # Windows 下独立窗口启动参数
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    
    subprocess.Popen(
        [sys.executable, main_file], 
        cwd=novel_reader_dir,
        creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS
    )
    print("✅ 启动指令已发出！")
    
    # 验证进程
    time.sleep(2)
    found = False
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cl = proc.info.get('cmdline', [])
            if cl and 'main.py' in ' '.join(cl):
                print(f"✅ 阅读器已成功运行！PID: {proc.info['pid']}")
                found = True
                break
        except: pass
    
    if not found:
        print("⚠️ 警告：进程未检测到，可能启动报错。请查看任务管理器或手动运行测试。")
        
except Exception as e:
    print(f"❌ 启动失败：{e}")