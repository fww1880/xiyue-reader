import subprocess, os, json
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🏗️ 在本地生成 Android 项目文件...")
# 使用 node 执行 npx cap init
node_path = r'C:\Program Files\nodejs\node.EXE'
npm_path = r'C:\Program Files\nodejs\npm.cmd'
# 先确保 @capacitor/cli 已安装
print("📦 检查 Capacitor CLI...")
installed = subprocess.run([npm_path, 'ls', '@capacitor/cli'], cwd=base_dir, capture_output=True, text=True)
if '@capacitor/cli' not in installed.stdout:
    print("安装 @capacitor/cli...")
    subprocess.run([npm_path, 'install', '@capacitor/core', '@capacitor/cli', '@capacitor/android'], cwd=base_dir, capture_output=True)
    print("✅ 安装完成")
else:
    print("✅ @capacitor/cli 已安装")
# 使用 node 直接调用 capacitor 的 API
print("\n📝 手动创建 Android 项目文件...")
# 创建 android 目录结构
android_dir = os.path.join(base_dir, 'android')
os.makedirs(android_dir, exist_ok=True)
# 创建 capacitor 需要的 android 项目文件
# 使用 node 脚本
node_script = """
const { init, add } = require('@capacitor/cli');
async function setup() {
    try {
        await init('XiyueReader', 'org.novalreader.xiyue', { webDir: 'dist', force: true });
        console.log('✅ Capacitor init 成功');
        await add('android', { force: true });
        console.log('✅ Android 平台添加成功');
    } catch (e) {
        console.error('❌ 错误:', e.message);
        console.error('堆栈:', e.stack);
    }
}
setup();
"""
script_path = os.path.join(base_dir, 'setup_capacitor.js')
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(node_script)
print("⚡ 运行 Capacitor 初始化脚本...")
result = subprocess.run([node_path, script_path], cwd=base_dir, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"❌ 错误: {result.stderr}")
    # 检查 android 目录是否已创建
    if os.path.exists(os.path.join(base_dir, 'android', 'app')):
        print("✅ android/app 目录已存在，可能已经初始化成功")
    else:
        print("❌ android 项目未生成，需要手动创建")
# 检查是否生成了 android 目录
android_app_dir = os.path.join(base_dir, 'android', 'app')
if os.path.exists(android_app_dir):
    print(f"\n✅ Android 项目已生成！")
    print(f"📁 {android_app_dir}")
    # 列出关键文件
    for root, dirs, files in os.walk(os.path.join(base_dir, 'android')):
        level = root.replace(base_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:
            print(f'{subindent}{file}')
else:
    print("❌ Android 项目未生成")
    print("\n💡 需要手动创建 Android 项目结构")