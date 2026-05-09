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
print("🚀 重启「喜阅」（测试书架+书签保存）...")
process = subprocess.Popen(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)
if process.poll() is None:
    print(f"✅ 喜阅启动成功！PID: {process.pid}")
else:
    print("❌ 启动失败，获取错误信息...")
    result = subprocess.run([sys.executable, main_file], cwd=novel_reader_dir, capture_output=True, text=True, timeout=5)
    print(f"错误：{result.stderr}")
print("\n📚 现在保存的内容：")
print("  ✅ 书架中的所有书籍（导入的书库）")
print("  ✅ 所有添加的书签（每个书籍都单独保存）")
print("  ✅ 文件夹展开/折叠状态")
print("  ✅ 当前打开的书籍 + 阅读进度")
print("  ✅ 字体设置、主题模式、窗口大小位置")