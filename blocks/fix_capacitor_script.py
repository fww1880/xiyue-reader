import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
node_path = r'C:\Program Files\nodejs\node.EXE'
# 改成 .cjs 后缀
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
script_path = os.path.join(base_dir, 'setup_capacitor.cjs')
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(node_script)
print("⚡ 运行 Capacitor 初始化脚本 (.cjs)...")
result = subprocess.run([node_path, script_path], cwd=base_dir, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(f"错误: {result.stderr}")
# 检查是否生成了 android 目录
android_app_dir = os.path.join(base_dir, 'android', 'app')
if os.path.exists(android_app_dir):
    print(f"\n✅ Android 项目已生成！")
    # 列出关键目录结构
    for root, dirs, files in os.walk(os.path.join(base_dir, 'android')):
        level = root.replace(base_dir, '').count(os.sep)
        if level > 3:  # 只显示前3层
            continue
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
else:
    print(f"\n❌ Android 项目未生成")
    # 检查是否有任何新目录
    android_dir = os.path.join(base_dir, 'android')
    if os.path.exists(android_dir):
        print(f"android 目录内容: {os.listdir(android_dir)}")