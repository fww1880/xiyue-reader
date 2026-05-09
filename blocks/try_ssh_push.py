import subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 先检查有没有 SSH key
print("🔍 检查 SSH key...")
res = subprocess.run(['ssh', '-T', 'git@github.com'], capture_output=True, text=True, timeout=10)
print(f"SSH 测试结果：{res.stdout}{res.stderr}")
# 尝试用 SSH 方式推送
print("\n🔄 尝试 SSH 方式推送...")
subprocess.run(['git', 'remote', 'set-url', 'origin', 'git@github.com:fww1880/xiyue-reader.git'], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print(f"\n🎉 SSH 推送成功！")
    print(f"🔗 https://github.com/fww1880/xiyue-reader")
else:
    print(f"\n⚠️ SSH 也失败了：\n{res.stderr}")
    # 恢复 HTTPS
    subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/fww1880/xiyue-reader.git'], cwd=base_dir)
    print("\n💡 老板，网络连接 GitHub 不太稳定，可能是需要挂代理或者用其他网络。")
    print("   您有代理或者 VPN 吗？有的话告诉我，我帮您配置一下！")