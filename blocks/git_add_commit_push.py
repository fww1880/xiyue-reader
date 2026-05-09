import subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 配置代理
print("🔧 配置代理：socks5://127.0.0.1:7890")
subprocess.run(['git', 'config', 'http.proxy', 'socks5://127.0.0.1:7890'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', 'https.proxy', 'socks5://127.0.0.1:7890'], cwd=base_dir, capture_output=True)
print("📝 添加文件...")
subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True)
print("✅ 添加完成，提交...")
res = subprocess.run(['git', 'commit', '-m', 'Initial commit: add xiyue reader with GitHub Pages'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit result: {res.returncode}")
print(res.stdout)
if res.stderr:
    print(res.stderr)
print("\n🚀 推送到 GitHub...")
push_res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if push_res.returncode == 0:
    print("\n🎉 推送成功！老板您太牛了！👏")
    print(f"🔗 仓库地址：https://github.com/fww1880/xiyue-reader")
    print(f"🔗 Actions 页面：https://github.com/fww1880/xiyue-reader/actions")
    print(f"🔗 部署后访问地址：https://fww1880.github.io/xiyue-reader/")
    print("\n⏳ GitHub Action 会自动编译部署，一般 2-5 分钟就能完成！")
    # 清除代理
    subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
    subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)
else:
    print(f"\n⚠️ 推送失败：\n{push_res.stderr}")
    # 清除代理
    subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
    subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)