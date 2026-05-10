import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
action_path = os.path.join(base_dir, '.github', 'workflows', 'build-android.yml')
print("📄 正在优化 build-android.yml...")
new_yml = """name: Build Android APK
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch: # 允许手动触发
jobs:
  build-apk:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            python3-pip \
            python3-setuptools \
            openjdk-17-jdk \
            autoconf \
            automake \
            build-essential \
            libssl-dev \
            libffi-dev \
            cmake \
            ninja-build \
            pkg-config \
            libgl1-mesa-dev \
            libgles2-mesa-dev \
            zlib1g-dev \
            libncurses5 \
            libncurses6 \
            libstdc++6 \
            libc6-dev \
            git \
            zip \
            unzip \
            wget \
            curl \
            python3-venv
            
      - name: Install Buildozer & Cython
        run: |
          python -m pip install --upgrade pip
          pip install buildozer==1.5.0 cython==3.0.10 packaging
          
      - name: Setup Android SDK
        run: |
          export ANDROID_HOME=$HOME/android-sdk
          mkdir -p $ANDROID_HOME
          cd $HOME
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
          unzip -q cmdline-tools.zip
          mkdir -p $ANDROID_HOME/cmdline-tools
          mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest
          export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
          yes | sdkmanager --licenses > /dev/null 2>&1
          sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"
          echo "ANDROID_HOME=$ANDROID_HOME" >> $GITHUB_ENV
          echo "PATH=$PATH" >> $GITHUB_ENV
          
      - name: Build APK with Buildozer
        run: |
          buildozer android debug
        env:
          CI: "true"
          ANDROID_HOME: ${{ env.ANDROID_HOME }}
          
      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: xiyue-apk
          path: bin/*.apk
          if-no-files-found: error
          
      - name: Create Release
        if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')
        uses: softprops/action-gh-release@v1
        with:
          files: bin/*.apk
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
with open(action_path, 'w', encoding='utf-8') as f:
    f.write(new_yml)
print("✅ build-android.yml 已优化完成！")
print("📋 主要改进：")
print("- 修复了 CI 环境下 deploy run 导致的失败")
print("- 增加了 CI=true 环境变量")
print("- 补充了更多系统依赖")
print("- 固定了 Buildozer 和 Cython 版本，提高稳定性")
print("- 优化了 SDK 安装步骤")
import subprocess
print("\n🚀 提交并推送修复...")
subprocess.run(['git', 'add', action_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: optimize buildozer CI config and remove deploy run'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
print(f"Push result: {push.returncode}")
if push.returncode == 0:
    print("🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"⚠️ 推送失败: {push.stderr}")