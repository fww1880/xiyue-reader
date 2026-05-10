import os, json
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 检查 GitHub Action 配置文件
action_path = os.path.join(base_dir, '.github', 'workflows', 'deploy.yml')
if os.path.exists(action_path):
    print(f"📄 找到 GitHub Action 文件: {action_path}")
    with open(action_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"内容预览：")
    print(content[:500])
else:
    print(f"❌ 没有找到 GitHub Action 文件")
    # 检查是否有其他配置文件
    workflows_dir = os.path.join(base_dir, '.github', 'workflows')
    if os.path.exists(workflows_dir):
        files = os.listdir(workflows_dir)
        print(f"📁 workflows 目录下的文件：{files}")
        for file in files:
            fp = os.path.join(workflows_dir, file)
            with open(fp, 'r', encoding='utf-8') as f:
                print(f"\n📄 {file} 内容：")
                print(f.read())