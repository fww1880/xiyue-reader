import subprocess
print("🔍 检查当前 Git 配置...")
# 检查远程仓库
res = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, cwd=r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj')
print(f"远程仓库：\n{res.stdout}")
# 检查分支
res = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True, cwd=r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj')
print(f"分支：\n{res.stdout}")
# 检查 Git 用户
res = subprocess.run(['git', 'config', '--global', 'user.name'], capture_output=True, text=True)
print(f"Git 用户名：{res.stdout.strip()}")
res = subprocess.run(['git', 'config', '--global', 'user.email'], capture_output=True, text=True)
print(f"Git 邮箱：{res.stdout.strip()}")