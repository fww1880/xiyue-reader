import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔧 再次修复 Capacitor init...")
# 尝试使用英文应用名，并且分步执行
new_yml = """name: Build Android APK
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
jobs:
  build-apk:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Build Vue project
        run: npm run build
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3
      - name: Install Capacitor
        run: |
          npm install @capacitor/core @capacitor/cli @capacitor/android
      - name: Initialize Capacitor
        run: |
          npx cap init "XiyueReader" "org.novalreader.xiyue" --web-dir dist --force
      - name: Add Android Platform
        run: |
          npx cap add android --force
      - name: Sync Capacitor
        run: npx cap sync android
      - name: Build Android APK
        run: |
          cd android && chmod +x gradlew && ./gradlew assembleDebug
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: android/app/build/outputs/apk/debug/*.apk
          if-no-files-found: error
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ 修复完成！")
print("📋 修复内容：")
print("- 使用英文名称 'XiyueReader' 避免编码问题")
print("- 添加 --force 参数强制覆盖已存在的配置")
print("- 将 init 和 add 分成两个独立步骤")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: use English app name and split init/add steps'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")