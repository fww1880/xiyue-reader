import subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🚀 开始推送...")
res = subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_dir, capture_output=True, text=True)
if res.returncode == 0:
    print(f"\n🎉 推送成功！")
    print(f"🔗 仓库地址：https://github.com/fww1880/xiyue-reader")
    print(f"🔗 Actions 页面：https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败：\n{res.stderr}")