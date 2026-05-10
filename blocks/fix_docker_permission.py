import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔧 修复 Docker 容器权限问题...")
new_yml = """name: Build Android APK
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:
jobs:
  build-apk:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Use Buildozer action
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          workdir: .
          build_mode: debug
          
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: ${{ steps.buildozer.outputs.apk_path }}
          if-no-files-found: error
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ 已切换到成熟的 GitHub Action 构建方案！")
print("📋 优势：")
print("- 使用现成的 ArtemSBulgakov/buildozer-action")
print("- 它处理好了 Docker、依赖、权限等问题")
print("- 我们只需要一行配置即可")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: use ArtemSBulgakov/buildozer-action for reliable build'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")