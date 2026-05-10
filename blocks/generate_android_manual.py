import subprocess, os, json, shutil
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
node_path = r'C:\Program Files\nodejs\node.EXE'
print("🏗️ 使用 Capacitor CLI 直接初始化...")
# 直接使用 npx.cmd 或 node_modules 中的 cap
# 先找到 cap 命令
cap_cmd = os.path.join(base_dir, 'node_modules', '.bin', 'cap.cmd')
if os.path.exists(cap_cmd):
    print(f"✅ 找到 cap 命令: {cap_cmd}")
    # 使用 cap.cmd 直接运行
    result = subprocess.run([cap_cmd, 'init', 'XiyueReader', 'org.novalreader.xiyue', '--web-dir', 'dist', '--force'], 
                          cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    if result.returncode == 0:
        print("\n✅ Capacitor init 成功！")
        # 添加 android 平台
        result2 = subprocess.run([cap_cmd, 'add', 'android', '--force'], 
                               cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
        print(f"Add android return code: {result2.returncode}")
        print(f"Stdout: {result2.stdout}")
        if result2.stderr:
            print(f"Stderr: {result2.stderr}")
else:
    print("❌ 没有找到 cap.cmd")
    # 尝试 npx.cmd
    npx_cmd = os.path.join(base_dir, 'node_modules', '.bin', 'npx.cmd')
    if os.path.exists(npx_cmd):
        print("尝试使用 npx...")
        result = subprocess.run([npx_cmd, 'cap', 'init', 'XiyueReader', 'org.novalreader.xiyue', '--web-dir', 'dist', '--force'],
                              cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")
# 检查 android 目录
android_dir = os.path.join(base_dir, 'android')
if os.path.exists(android_dir):
    print(f"\n📁 android 目录内容:")
    items = os.listdir(android_dir)
    for item in items:
        print(f"  {item}")
    # 检查是否有 build.gradle
    build_gradle = os.path.join(android_dir, 'build.gradle')
    if os.path.exists(build_gradle):
        print(f"✅ build.gradle 存在")
else:
    print(f"\n❌ android 目录不存在")