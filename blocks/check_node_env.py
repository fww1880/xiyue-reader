import subprocess
print("🔍 检查 node 环境...")
# 检查 node
res = subprocess.run(['node', '--version'], capture_output=True, text=True)
if res.returncode == 0:
    print(f"✅ Node 版本：{res.stdout.strip()}")
else:
    print("❌ Node 未安装！")
# 检查 npm
res = subprocess.run(['npm', '--version'], capture_output=True, text=True)
if res.returncode == 0:
    print(f"✅ npm 版本：{res.stdout.strip()}")
else:
    print("❌ npm 未找到")
# 检查 pnpm
res = subprocess.run(['pnpm', '--version'], capture_output=True, text=True)
if res.returncode == 0:
    print(f"✅ pnpm 版本：{res.stdout.strip()}")
else:
    print("❌ pnpm 未找到")
# 检查 yarn
res = subprocess.run(['yarn', '--version'], capture_output=True, text=True)
if res.returncode == 0:
    print(f"✅ yarn 版本：{res.stdout.strip()}")
else:
    print("❌ yarn 未找到")