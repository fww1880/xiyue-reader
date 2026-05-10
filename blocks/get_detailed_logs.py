import subprocess, os, json
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 使用 GitHub CLI 获取日志
print("📋 尝试获取 GitHub Action 日志...")
# 检查是否有 gh CLI
gh_path = subprocess.run(['where', 'gh'], capture_output=True, text=True)
if gh_path.returncode == 0:
    print("✅ 找到 GitHub CLI")
    # 获取最新的 workflow run 日志
    log_res = subprocess.run(['gh', 'run', 'list', '--limit', '1', '--json', 'databaseId,status,conclusion,headBranch'], 
                           cwd=base_dir, capture_output=True, text=True)
    print(f"最近运行记录: {log_res.stdout}")
else:
    print("❌ 没有安装 GitHub CLI，无法直接获取日志")
    print("\n💡 请老板手动查看日志：")
    print("1. 打开 https://github.com/fww1880/xiyue-reader/actions")
    print("2. 点击最新的 Build Android APK 任务")
    print("3. 点击失败的 build-apk 步骤")
    print("4. 查看完整的错误日志并告诉我")
print("\n🔍 检查 buildozer.spec 配置...")
spec_path = os.path.join(base_dir, 'buildozer.spec')
with open(spec_path, 'r', encoding='utf-8') as f:
    content = f.read()
print(content)