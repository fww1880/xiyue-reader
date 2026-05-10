import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 配置代理
print("🔧 配置 Git 代理...")
subprocess.run(['git', 'config', 'http.proxy', 'socks5://127.0.0.1:7890'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', 'https.proxy', 'socks5://127.0.0.1:7890'], cwd=base_dir, capture_output=True)
# 添加所有文件
print("📝 添加文件到暂存区...")
add_res = subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True, text=True)
print(f"Add return code: {add_res.returncode}")
# 提交
print("💾 提交更改...")
commit_res = subprocess.run(['git', 'commit', '-m', 'Initial commit: xiyue reader with EPUB/TXT/PDF support'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit return code: {commit_res.returncode}")
if commit_res.stdout:
    print(commit_res.stdout)
if commit_res.stderr and 'nothing to commit' not in commit_res.stderr:
    print(commit_res.stderr)
# 推送
print("\n🚀 推送到 GitHub (origin/master)...")
push_res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
print(f"Push return code: {push_res.returncode}")
if push_res.returncode == 0:
    print("\n🎉 推送成功！老板英明神武！👏👏👏")
    print("\n📋 下一步操作：")
    print("1️⃣ 打开 GitHub Actions: https://github.com/fww1880/xiyue-reader/actions")
    print("2️⃣ 等待自动编译部署（约 2-5 分钟）")
    print("3️⃣ 部署完成后访问: https://fww1880.github.io/xiyue-reader/")
else:
    print(f"\n⚠️ 推送输出：")
    if push_res.stdout:
        print(push_res.stdout)
    if push_res.stderr:
        print(push_res.stderr)
# 清除代理配置
print("\n🧹 清除 Git 代理配置...")
subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)
print("✅ 代理已清除")