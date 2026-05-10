import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 确保没有代理配置
print("🧹 确保清除所有代理配置...")
subprocess.run(['git', 'config', '--unset', 'http.proxy'], cwd=base_dir, capture_output=True)
subprocess.run(['git', 'config', '--unset', 'https.proxy'], cwd=base_dir, capture_output=True)
# 再次尝试推送
print("\n🚀 直接推送到 GitHub (不使用代理)...")
push_res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True, timeout=60)
print(f"Push return code: {push_res.returncode}")
if push_res.returncode == 0:
    print("\n🎉 推送成功！老板威武！👏👏👏")
    print("\n📋 下一步操作：")
    print("1️⃣ 打开 GitHub Actions: https://github.com/fww1880/xiyue-reader/actions")
    print("2️⃣ 等待自动编译部署（约 2-5 分钟）")
    print("3️⃣ 部署完成后访问: https://fww1880.github.io/xiyue-reader/")
else:
    print(f"\n⚠️ 推送失败信息：")
    if push_res.stdout:
        print(push_res.stdout)
    if push_res.stderr:
        print(push_res.stderr)
    print("\n💡 建议：")
    print("- 检查 VPN 是否正常连接")
    print("- 尝试在浏览器访问 github.com 确认网络通畅")
    print("- 如果必须使用代理，请确认正确的代理地址和端口")