import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
cap_cmd = os.path.join(base_dir, 'node_modules', '.bin', 'cap.cmd')
print("🏗️ 初始化 Capacitor（去掉 --force）...")
# 先 cap init
result = subprocess.run([cap_cmd, 'init', 'XiyueReader', 'org.novalreader.xiyue', '--web-dir', 'dist'], 
                      cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
print(f"Init return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
if result.stderr:
    print(f"Stderr: {result.stderr}")
if result.returncode == 0:
    print("\n✅ Capacitor init 成功！")
    # 添加 android 平台
    result2 = subprocess.run([cap_cmd, 'add', 'android'], 
                           cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
    print(f"\nAdd android return code: {result2.returncode}")
    print(f"Stdout: {result2.stdout}")
    if result2.stderr:
        print(f"Stderr: {result2.stderr}")
    if result2.returncode == 0:
        print("\n✅ Android 平台添加成功！")
    else:
        print("\n❌ Android 平台添加失败")
else:
    print("\n❌ Capacitor init 失败")
# 检查 android 目录
android_dir = os.path.join(base_dir, 'android')
if os.path.exists(android_dir):
    print(f"\n📁 android 目录内容:")
    items = os.listdir(android_dir)
    for item in items:
        print(f"  {item}")
    # 检查关键文件
    build_gradle = os.path.join(android_dir, 'build.gradle')
    if os.path.exists(build_gradle):
        print(f"✅ build.gradle 存在")
    app_dir = os.path.join(android_dir, 'app')
    if os.path.exists(app_dir):
        print(f"✅ app 目录存在")
else:
    print(f"\n❌ android 目录不存在")