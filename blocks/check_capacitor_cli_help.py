import subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("📋 检查 Capacitor CLI 帮助信息...")
# 检查 npx cap 是否可用
result = subprocess.run(['npx', 'cap', '--help'], cwd=base_dir, capture_output=True, text=True)
print(f"Return code: {result.returncode}")
if result.returncode == 0:
    print("✅ npx cap 可用")
    print(result.stdout[:1000])
else:
    print(f"❌ npx cap 不可用: {result.stderr}")
    # 检查 node_modules 中是否有 capacitor
    cap_path = os.path.join(base_dir, 'node_modules', '@capacitor', 'cli')
    if os.path.exists(cap_path):
        print(f"✅ @capacitor/cli 已安装: {cap_path}")
        # 查看 package.json 中的 bin 配置
        import json
        with open(os.path.join(cap_path, 'package.json'), 'r') as f:
            pkg = json.load(f)
        print(f"版本: {pkg.get('version', 'unknown')}")
        print(f"bin: {pkg.get('bin', 'none')}")
    else:
        print("❌ @capacitor/cli 未安装")
print("\n🔍 检查 capacitor.config.json...")
config_path = os.path.join(base_dir, 'capacitor.config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        print(f.read())