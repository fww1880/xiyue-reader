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
print("🚀 重启「喜阅」（书架全护眼绿色）...")
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 验证启动
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            print(f"✅ 喜阅启动成功！PID: {proc.info['pid']}")
            break
    except: pass
print("\n🎨 修改完成：")
print("  📚 我的书架 → 整体背景：护眼豆沙绿 #CCE8CF")
print("  📋 目录标签 → 背景：浅绿 #A5D6A7，文字：深绿 #2E7D32")
print("  📑 书签标签 → 背景：浅绿 #A5D6A7，文字：深绿 #2E7D32")
print("  📜 目录/书签列表 → 背景：浅绿 #DCEDC8，选中/悬停都为递进绿色")
print("\n💡 完全统一护眼色调，长时间看更舒服！")