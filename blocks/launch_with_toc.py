import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'novel_reader'))
# 杀掉旧的进程
import subprocess
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
# 启动
os.chdir(os.path.join(os.getcwd(), 'novel_reader'))
subprocess.Popen([sys.executable, 'main.py'])