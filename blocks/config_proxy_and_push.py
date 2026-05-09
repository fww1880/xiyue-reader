import subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔧 配置 Git HTTP/HTTPS 代理：127.0.0.1:7890")
subprocess.run(['git', 'config', 'http.proxy', 'http://127.0.0.1:7890'], cwd=base_dir, capture_output=True, text=True)
subprocess.run(['git', 'config', 'https.proxy', 'http://127.0.0.1:7890'], cwd=base_dir, capture_output=True, text=True)
print("✅ 代理配置完成，开始推送...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print(f"\n🎉 推送成功！老板您领导有方！👏")
    print(f"🔗 仓库地址：https://github.com/fww1880/xiyue-reader")
    print(f"🔗 Actions 页面：https://github.com/fww1880/xiyue-reader/actions")
    print("\n接下来 GitHub Action 会自动编译部署到 gh-pages 分支，")
    print("几分钟后您就能在 https://fww1880.github.io/xiyue-reader/ 访问到阅读器了！")
    # 清除代理配置
    subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
    subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)
else:
    print(f"\n⚠️ 推送失败：\n{res.stderr}")