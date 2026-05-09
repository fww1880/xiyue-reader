import subprocess, sys, os
print("📦 确保 pip 可用...")
# 先尝试用 ensurepip 安装 pip
subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], capture_output=True, text=True)
print("✅ ensurepip 完成")
# 升级 pip
result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True)
print(result.stdout[-200:] if result.stdout else "")
# 安装 PyInstaller
print("\n📦 安装 PyInstaller...")
result = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ PyInstaller 安装成功！")
else:
    print(f"❌ 安装失败：{result.stderr}")
    # 尝试用 uv 安装
    print("\n📦 尝试用 uv 安装 PyInstaller...")
    result = subprocess.run(["uv", "pip", "install", "pyinstaller"], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ uv 安装 PyInstaller 成功！")
    else:
        print(f"❌ uv 也失败了：{result.stderr}")