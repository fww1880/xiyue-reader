import os
import sys
import subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print(f"🚀 启动阅读器...")
print(f"工作目录: {novel_reader_dir}")
print(f"主程序: {main_file}")
# 直接启动
try:
    process = subprocess.Popen([sys.executable, main_file], 
                               cwd=novel_reader_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    print("✅ 阅读器进程已启动")
    # 等待几秒看是否有输出
    import time
    time.sleep(3)
    stdout, stderr = process.communicate(timeout=1)
    if stdout:
        print(f"📤 标准输出: {stdout.decode('utf-8')}")
    if stderr:
        print(f"📤 错误输出: {stderr.decode('utf-8')}")
except Exception as e:
    print(f"❌ 启动失败: {e}")