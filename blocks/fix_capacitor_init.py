import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔧 修复 Capacitor init 在 CI 环境的问题...")
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
      - name: Initialize Capacitor and add Android
        run: |
          npx cap init 喜阅阅读器 org.novalreader.xiyue --web-dir dist --no-git
          npx cap add android
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
print("- 添加了 --no-git 参数，避免 CI 环境中的 git 问题")
print("- 添加了 actions/setup-java@v4 步骤")
print("- 添加了 android-actions/setup-android@v3 步骤")
print("- 合并了 init 和 add 步骤")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: add --no-git flag and setup Java/Android SDK for Capacitor'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")