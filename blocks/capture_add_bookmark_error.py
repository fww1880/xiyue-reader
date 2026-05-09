import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 先启动阅读器
import psutil, time
for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        if 'main.py' in ' '.join(proc.info.get('cmdline', [])):
            proc.kill()
    except: pass
time.sleep(1)
subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
time.sleep(2)
# 模拟添加书签的错误
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查看 add_bookmark 方法
start = content.find('def add_bookmark')
if start != -1:
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    method = content[start:end]
    print("🔍 add_bookmark 完整方法：")
    print(method)
    # 检查可能的问题
    if 'self.get_position_preview' in method:
        print("✅ 使用了 get_position_preview")
    else:
        print("❌ 没有调用 get_position_preview")