import subprocess
import sys
# 需要安装的依赖包
dependencies = [
    'PyQt5',
    'chardet',
    'requests',
    'beautifulsoup4',
    'PyPDF2',
    'lxml'
]
print("开始安装依赖包...")
for dep in dependencies:
    print(f"\n正在安装 {dep}...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ {dep} 安装成功")
    else:
        print(f"✗ {dep} 安装失败，错误信息：\n{result.stderr}")
print("\n所有依赖安装完成！")
utils.set_state(success=True)