import os, subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
username = 'fww1880'
repo_name = 'xiyue-reader'
remote_url = f'https://github.com/{username}/{repo_name}.git'
print(f"🔧 更新远程仓库地址为：{remote_url}")
# 更新远程仓库
subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], cwd=base_dir, capture_output=True)
# 确认更新
res = subprocess.run(['git', 'remote', '-v'], cwd=base_dir, capture_output=True, text=True)
print(f"✅ 更新后：\n{res.stdout}")
# 推送
print("\n🚀 开始推送...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print(f"\n🎉 推送成功！")
    print(f"🔗 仓库地址：{remote_url}")
    print(f"🔗 Actions 页面：https://github.com/{username}/{repo_name}/actions")
else:
    print(f"\n⚠️ 推送失败：\n{res.stderr}")
    print("\n💡 如果提示 \"Authentication failed\"，说明需要 Personal Access Token：")
    print("""
解决方案（用 Token 认证）：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 "repo" 权限
4. 点击 "Generate token" 然后复制 Token
5. 在命令行执行：
   cd C:\\Users\\86139\\aipywork\\CapEwGvvipaKTj79zEPUj
   git remote set-url origin https://YOUR_TOKEN@github.com/fww1880/xiyue-reader.git
   git push -u origin master
""")