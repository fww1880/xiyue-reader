import subprocess
import sys
import os
# 切换到novel_reader目录并启动
reader_path = os.path.join(os.getcwd(), 'novel_reader', 'main.py')
print(f"启动阅读器: {reader_path}")
# 使用pythonw.exe后台启动，不阻塞终端
python_exe = sys.executable
process = subprocess.Popen(
    [python_exe, reader_path],
    cwd=os.path.join(os.getcwd(), 'novel_reader'),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print(f"✅ 阅读器已启动，进程ID: {process.pid}")
print("请查看桌面上的阅读器窗口！")
utils.set_state(success=True, pid=process.pid)