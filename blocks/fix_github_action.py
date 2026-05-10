import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print(f"📄 修复 GitHub Action 文件: {action_path}")
with open(action_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 替换 v3 为 v4
new_content = content.replace('actions/upload-artifact@v3', 'actions/upload-artifact@v4')
# 检查还有没有其他 v3 需要更新
new_content = new_content.replace('actions/checkout@v3', 'actions/checkout@v4')
print(f"✅ 已将 upload-artifact 从 v3 更新到 v4")
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"✅ 文件已更新")
# 显示更新后的部分
print(f"\n📋 更新后的关键部分：")
lines = new_content.split('\n')
for i, line in enumerate(lines):
    if 'upload-artifact' in line or 'checkout' in line:
        print(f"行 {i+1}: {line}")
print("\n🚀 现在重新提交并推送修复后的 Action 文件...")
# 提交修复
import subprocess
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
commit_res = subprocess.run(['git', 'commit', '-m', 'Fix: update actions/upload-artifact from v3 to v4'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit result: {commit_res.stdout}")
push_res = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
print(f"Push result code: {push_res.returncode}")
if push_res.returncode == 0:
    print("\n🎉 修复已提交并推送！GitHub Action 会自动重新运行！")
    print(f"🔗 Actions 页面: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push_res.stderr}")