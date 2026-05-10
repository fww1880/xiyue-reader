import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🔄 切换到 Capacitor 构建方案（专为 Vue 项目设计）...")
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
      - name: Copy Capacitor config
        run: npx cap copy android
      - name: Build Android APK
        run: npx cap open android || npx cap sync android && cd android && ./gradlew assembleDebug
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: android/app/build/outputs/apk/debug/*.apk
          if-no-files-found: error
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ 已切换到 Capacitor 方案！")
print("\n📋 还需要初始化 Capacitor Android 项目...")
# 先安装 @capacitor/cli 和 @capacitor/android
import subprocess
print("📦 安装 Capacitor...")
npm_path = r'C:\Program Files\nodejs\npm.cmd'
install_res = subprocess.run([npm_path, 'install', '@capacitor/cli', '@capacitor/android', '@capacitor/core'], 
                           cwd=base_dir, capture_output=True, text=True)
print(f"安装结果: {install_res.returncode}")
if install_res.returncode == 0:
    print("✅ Capacitor 安装成功！")
    # 初始化 Android 项目
    print("\n📱 初始化 Android 平台...")
    init_res = subprocess.run(['npx', 'cap', 'init', '喜阅阅读器', 'org.novalreader.xiyue'], 
                            cwd=base_dir, capture_output=True, text=True)
    print(f"初始化结果: {init_res.returncode}")
    if init_res.stdout:
        print(init_res.stdout)
    if init_res.stderr:
        print(init_res.stderr)
    # 添加 Android 平台
    print("\n📱 添加 Android 平台...")
    add_res = subprocess.run(['npx', 'cap', 'add', 'android'], 
                           cwd=base_dir, capture_output=True, text=True)
    print(f"添加结果: {add_res.returncode}")
    if add_res.stdout:
        print(add_res.stdout)
    if add_res.stderr:
        print(add_res.stderr)
    # 同步
    print("\n🔄 同步...")
    sync_res = subprocess.run(['npx', 'cap', 'sync', 'android'], 
                            cwd=base_dir, capture_output=True, text=True)
    print(f"同步结果: {sync_res.returncode}")
    if sync_res.stdout:
        print(sync_res.stdout)
    if sync_res.stderr:
        print(sync_res.stderr)
else:
    print(f"❌ 安装失败: {install_res.stderr}")
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', '.'], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: switch to Capacitor for Vue APK build'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")