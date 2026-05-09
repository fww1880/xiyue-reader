import os
# 创建工作流目录
workflow_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\.github\workflows'
os.makedirs(workflow_dir, exist_ok=True)
# GitHub Actions 工作流配置
workflow_content = '''name: Build Android APK
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
        uses: actions/checkout@v3
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
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
            zlib1g-dev
            
      - name: Install Buildozer
        run: |
          pip3 install --upgrade pip
          pip3 install buildozer cython packaging
        
      - name: Setup Android environment
        run: |
          export ANDROID_HOME=$HOME/android-sdk
          mkdir -p $ANDROID_HOME
          cd $HOME
          wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
          unzip -q cmdline-tools.zip
          mkdir -p $ANDROID_HOME/cmdline-tools
          mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest
          export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
          yes | sdkmanager --licenses
          sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2"
          
      - name: Build APK with Buildozer
        run: |
          buildozer android debug deploy run
        env:
          ANDROID_HOME: ${{ env.ANDROID_HOME }}
          
      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
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
'''
workflow_path = os.path.join(workflow_dir, 'build-android.yml')
with open(workflow_path, 'w', encoding='utf-8') as f:
    f.write(workflow_content)
print(f"✅ 已创建 GitHub Actions 工作流：{workflow_path}")