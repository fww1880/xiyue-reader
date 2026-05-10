import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔍 分析 Capacitor 构建错误...")
# 检查 capacitor.config.json
config_path = os.path.join(base_dir, 'capacitor.config.json')
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = f.read()
    print(f"✅ capacitor.config.json 内容：")
    print(config)
else:
    print("❌ 没有找到 capacitor.config.json")
# 检查 dist 目录是否存在（Capacitor 需要先 build）
dist_path = os.path.join(base_dir, 'dist')
if os.path.exists(dist_path):
    files = os.listdir(dist_path)
    print(f"\n✅ dist 目录存在，包含 {len(files)} 个文件/文件夹")
    print(f"前 10 个：{files[:10]}")
else:
    print(f"\n❌ dist 目录不存在！这可能是问题所在！")
    print("GitHub Action 会先执行 npm run build 创建 dist 目录")
# 检查 package.json 中的 scripts
pkg_path = os.path.join(base_dir, 'package.json')
with open(pkg_path, 'r', encoding='utf-8') as f:
    import json
    pkg = json.load(f)
print(f"\n📋 package.json scripts:")
for key, value in pkg.get('scripts', {}).items():
    print(f"  {key}: {value}")
print("\n💡 可能的错误原因：")
print("1. npx cap init 命令在 CI 环境中需要额外参数")
print("2. Android SDK 环境变量未正确设置")
print("3. Gradle 构建失败")
print("\n🔗 请老板查看完整日志并告诉我具体的错误信息！")
print("打开：https://github.com/fww1880/xiyue-reader/actions")