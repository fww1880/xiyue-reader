import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("🐳 正在切换到 Docker 构建方案...")
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
    container:
      image: kivy/buildozer:latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Android SDK
        run: |
          export ANDROID_HOME=$HOME/android-sdk
          mkdir -p $ANDROID_HOME/cmdline-tools/latest
          cd /tmp
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
          unzip -q cmdline-tools.zip
          mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest/
          export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
          yes | sdkmanager --licenses > /dev/null 2>&1 || true
          sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"
          echo "ANDROID_HOME=$ANDROID_HOME" >> $GITHUB_ENV
          
      - name: Build APK with Buildozer
        run: |
          # 确保在正确的目录
          ls -la
          # 运行构建（仅 debug 模式）
          buildozer android debug
        env:
          CI: "true"
          ANDROID_HOME: /root/android-sdk
          
      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: bin/*.apk
          if-no-files-found: error
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ 已切换为 Docker 构建方案！")
print("📋 优势：")
print("- 使用官方 Kivy Buildozer Docker 镜像")
print("- 预装了所有依赖，避免 apt-get 错误")
print("- 环境隔离，构建更稳定")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: use Docker container for stable APK build'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
    print("\n⏱️ 这次应该能成功了！Docker 镜像已经预装了所有依赖～")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")