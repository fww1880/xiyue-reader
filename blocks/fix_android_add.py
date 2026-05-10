import subprocess, os, shutil
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
cap_cmd = os.path.join(base_dir, 'node_modules', '.bin', 'cap.cmd')
print("🗑️ 删除旧的 android 目录...")
android_dir = os.path.join(base_dir, 'android')
if os.path.exists(android_dir):
    shutil.rmtree(android_dir)
    print("✅ 已删除")
print("🏗️ 重新添加 Android 平台...")
result = subprocess.run([cap_cmd, 'add', 'android'], 
                      cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
if result.stderr:
    print(f"Stderr: {result.stderr}")
if result.returncode == 0:
    print("\n✅✅✅ Android 平台添加成功！")
else:
    print("\n❌ 添加失败")
# 检查 android 目录
if os.path.exists(android_dir):
    print(f"\n📁 android 目录内容:")
    items = os.listdir(android_dir)
    for item in items:
        print(f"  {item}")
    build_gradle = os.path.join(android_dir, 'build.gradle')
    if os.path.exists(build_gradle):
        print(f"✅ build.gradle 存在")
    app_dir = os.path.join(android_dir, 'app')
    if os.path.exists(app_dir):
        print(f"✅ app 目录存在")
        app_build = os.path.join(app_dir, 'build.gradle')
        if os.path.exists(app_build):
            print(f"✅ app/build.gradle 存在")
else:
    print(f"\n❌ android 目录不存在")