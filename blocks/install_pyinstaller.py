import subprocess, sys, os
print("📦 安装 PyInstaller...")
result = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ PyInstaller 安装成功！")
else:
    print(f"❌ 安装失败：{result.stderr}")