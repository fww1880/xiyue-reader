import os, subprocess, sys
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🚀 开始推送到 GitHub...")
# 1. 检查 git 是否已初始化
print("\n📌 第 1 步：检查 Git 状态")
res = subprocess.run(['git', 'status', '--porcelain'], cwd=base_dir, capture_output=True, text=True)
if res.stdout:
    print("✅ 有未提交的更改")
    print("📋 待提交文件：")
    print(res.stdout)
else:
    print("⚠️ 没有未提交的更改，可能已经提交过了")
# 2. 添加文件
print("\n📌 第 2 步：添加文件")
res = subprocess.run(['git', 'add', '-A'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print("✅ 文件添加成功")
else:
    print(f"❌ 添加失败：{res.stderr}")
# 3. 提交
print("\n📌 第 3 步：提交文件")
res = subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print("✅ 提交成功")
elif "nothing to commit" in res.stderr or "nothing to commit" in res.stdout:
    print("✅ 没有新的更改需要提交")
else:
    print(f"提交结果：{res.stdout or res.stderr}")
# 4. 设置远程仓库
print("\n📌 第 4 步：设置远程仓库")
# 先检查远程仓库
res = subprocess.run(['git', 'remote', '-v'], cwd=base_dir, capture_output=True, text=True)
if 'origin' in res.stdout:
    print("✅ 远程仓库已存在")
else:
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/86139/xiyue-reader.git'], cwd=base_dir, capture_output=True)
    print("✅ 已添加远程仓库")
# 5. 检查分支名
print("\n📌 第 5 步：检查分支名")
res = subprocess.run(['git', 'branch', '--show-current'], cwd=base_dir, capture_output=True, text=True)
branch = res.stdout.strip()
print(f"当前分支：{branch}")
if not branch:
    # 可能没有分支，创建一个
    print("⚠️ 没有分支，创建 main 分支")
    subprocess.run(['git', 'checkout', '-b', 'main'], cwd=base_dir, capture_output=True)
    branch = 'main'
# 6. 推送
print(f"\n📌 第 6 步：推送到 GitHub（分支：{branch}）")
print("⏳ 正在推送，请稍候...")
# 使用环境变量避免编码问题
env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'
res = subprocess.run(['git', 'push', '-u', 'origin', branch], cwd=base_dir, capture_output=True, text=True, env=env)
if res.returncode == 0:
    print("\n🎉 推送成功！")
    print(f"🔗 仓库地址：https://github.com/86139/xiyue-reader.git")
    print(f"🔗 Actions 页面：https://github.com/86139/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败：{res.stderr}")
    print("\n💡 解决方案：")
    print("  由于 GitHub 已不再支持密码认证，请使用 Personal Access Token：")
    print("  1. 访问 https://github.com/settings/tokens")
    print("  2. 点击 'Generate new token' → 'Generate new token (classic)'")
    print("  3. 勾选 repo 权限")
    print("  4. 生成 Token 并复制")
    print("  5. 在命令行执行以下命令：")
    print(f"     cd {base_dir}")
    print("     git remote set-url origin https://TOKEN@github.com/86139/xiyue-reader.git")
    print("     git push -u origin main")
    print("\n  或者使用 GitHub CLI（推荐）：")
    print("     1. 安装 GitHub CLI：winget install GitHub.cli")
    print("     2. 登录：gh auth login")
    print("     3. 推送：git push -u origin main")