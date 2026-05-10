import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔧 修复 buildozer-action 参数错误...")
# 查阅文档后确定正确的参数
new_yml = """name: Build Android APK
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true  # 消除 Node.js 20 警告
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
          # 默认就是 debug 模式，不需要 build_mode 参数
          # buildozer_version: '1.5.0'  # 可选指定版本
          
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: ${{ steps.buildozer.outputs.apk_path }}
          if-no-files-found: error
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ 修复完成！")
print("📋 修复内容：")
print("- 删除了不支持的 'build_mode' 参数")
print("- 增加了 FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true 环境变量")
print("- 消除了 Node.js 20 警告")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: remove unsupported build_mode param and set Node.js 24'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")