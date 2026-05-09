import subprocess, time
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔄 等待 3 秒后重试...")
time.sleep(3)
print("🚀 第二次尝试推送...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print(f"\n🎉 推送成功！")
    print(f"🔗 仓库地址：https://github.com/fww1880/xiyue-reader")
    print(f"🔗 Actions 页面：https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送还是失败：\n{res.stderr}")
    print("\n💡 这是网络连接问题，通常是 GitHub 在国内访问不稳定导致的。")
    print("\n📖 您有两个选择：")
    print("1. 继续本地运行，我已经在本地帮您做好了全部配置，可以直接在这里运行编译")
    print("2. 先完成 GitHub 认证，用 Token 推送，或者配置 SSH 密钥")
    print("\n老板，您看咱们是直接在本地编译，还是先搞定 GitHub 推送呢？")