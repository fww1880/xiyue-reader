import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
result = subprocess.run([sys.executable, main_file], capture_output=True, text=True, timeout=5)
print("返回码:", result.returncode)
print("❌ 错误：")
print(result.stderr)