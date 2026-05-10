import os, json
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("📄 创建 Capacitor 配置文件...")
# 创建 capacitor.config.json
capacitor_config = {
    "appId": "org.novalreader.xiyue",
    "appName": "喜阅阅读器",
    "webDir": "dist",
    "bundledWebRuntime": False,
    "server": {
        "androidScheme": "https"
    }
}
config_path = os.path.join(base_dir, 'capacitor.config.json')
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(capacitor_config, f, indent=2)
print("✅ 创建 capacitor.config.json")
# 更新 GitHub Action 配置 - 使用更稳定的方案
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
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
      - name: Install Capacitor
        run: |
          npm install @capacitor/core @capacitor/cli @capacitor/android
      - name: Initialize Capacitor Android
        run: |
          npx cap init 喜阅阅读器 org.novalreader.xiyue --web-dir dist
      - name: Add Android platform
        run: |
          npx cap add android
      - name: Sync Capacitor
        run: |
          npx cap sync android
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
print("✅ 更新 GitHub Action 配置")
print("\n📋 现在清理 buildozer.spec（不再需要）...")
spec_path = os.path.join(base_dir, 'buildozer.spec')
if os.path.exists(spec_path):
    os.remove(spec_path)
    print("✅ 已删除 buildozer.spec")
print("\n🚀 提交并推送...")
import subprocess
subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: switch to Capacitor for proper Vue APK building'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
    print("\n⏱️ 这次构建预计需要 5-8 分钟（Capacitor 比 Buildozer 快很多！）")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")