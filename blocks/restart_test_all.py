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
# 启动新进程（带输出以便调试）
print("🚀 重启「喜阅」（测试书库+书签保存）...")
process = subprocess.Popen(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(3)
if process.poll() is None:
    print(f"✅ 喜阅启动成功！PID: {process.pid}")
else:
    stdout, stderr = process.communicate()
    print(f"❌ 启动失败：{stderr[-500:]}")
print("\n💾 现在的完整保存逻辑：")
print("  1️⃣ 导入书籍 → 实时更新 bookshelf_data")
print("  2️⃣ 添加/删除书签 → 实时保存到对应书籍的 key")
print("  3️⃣ 关闭窗口 → 保存 bookshelf_data + 所有书签 + 其他状态")
print("  4️⃣ 启动应用 → 恢复书库 + 加载所有书的书签 + 恢复其他状态")