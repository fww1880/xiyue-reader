import os
import sys
import subprocess
# 安装缺失依赖
print("📦 安装缺失依赖...")
deps = ['chardet', 'beautifulsoup4', 'PyPDF2']
for dep in deps:
    result = subprocess.run(['uv', 'pip', 'install', dep], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ {dep} 安装成功")
    else:
        print(f"  ❌ {dep} 安装失败: {result.stderr}")
# 启动阅读器
print("\n🚀 启动阅读器...")
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
try:
    process = subprocess.Popen([sys.executable, main_file], 
                               cwd=novel_reader_dir)
    print("✅ 阅读器已启动！请查看桌面窗口。")
except Exception as e:
    print(f"❌ 启动失败: {e}")