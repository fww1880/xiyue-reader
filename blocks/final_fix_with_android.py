import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔧 最终修复 GitHub Action 配置...")
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
          npx cap init XiyueReader org.novalreader.xiyue --web-dir dist
      - name: Remove old android dir if exists
        run: |
          if [ -d "android" ]; then rm -rf android; fi
      - name: Add Android Platform
        run: |
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
print("✅ Action 配置已更新！")
print("📋 关键修复：在 cap add android 之前先删除旧的 android 目录")
import subprocess
print("\n🚀 提交并推送（包括生成的 android 项目文件）...")
subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: remove old android dir before adding platform'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉🎉🎉 所有文件已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
    print("\n💡 这次应该能成功了！Android 项目文件已包含在仓库中")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")