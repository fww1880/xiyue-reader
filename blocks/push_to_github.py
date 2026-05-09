import os, subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🚀 开始推送到 GitHub...")
# 1. 初始化 Git
print("\n📌 第 1 步：初始化 Git 仓库")
res = subprocess.run(['git', 'init'], cwd=base_dir, capture_output=True, text=True)
print(res.stdout if res.stdout else res.stderr)
# 2. 配置 Git 用户信息（如果未配置）
print("\n📌 第 2 步：配置 Git 用户信息")
subprocess.run(['git', 'config', '--global', 'user.name', 'xiyue-reader'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', '--global', 'user.email', 'xiyue@novalreader.org'], cwd=base_dir, capture_output=True)
print("✅ 已配置 Git 用户信息")
# 3. 添加所有文件
print("\n📌 第 3 步：添加文件到暂存区")
res = subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print("✅ 文件添加成功")
else:
    print(f"⚠️ {res.stderr}")
# 4. 提交
print("\n📌 第 4 步：提交文件")
res = subprocess.run(['git', 'commit', '-m', 'Initial commit: 喜阅阅读器'], cwd=base_dir, capture_output=True, text=True)
print(res.stdout if res.stdout else res.stderr)
# 5. 关联远程仓库
print("\n📌 第 5 步：关联远程仓库")
res = subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/86139/xiyue-reader.git'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print("✅ 远程仓库关联成功")
else:
    # 可能已存在，尝试更新
    subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/86139/xiyue-reader.git'], cwd=base_dir, capture_output=True)
    print("✅ 远程仓库 URL 已更新")
# 6. 推送
print("\n📌 第 6 步：推送到 GitHub")
print("⏳ 正在推送（可能需要输入 GitHub 账号密码）...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=base_dir, capture_output=True, text=True)
print(res.stdout if res.stdout else res.stderr)
if res.returncode == 0:
    print("\n🎉 推送成功！")
else:
    print("\n⚠️ 推送遇到问题，请按以下方式处理：")
    print("  1. 使用 Personal Access Token 代替密码：")
    print("     https://github.com/settings/tokens")
    print("  2. 创建 Token 后执行：")
    print("     git remote set-url origin https://TOKEN@github.com/86139/xiyue-reader.git")
    print("     git push -u origin main")