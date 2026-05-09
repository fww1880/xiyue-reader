import subprocess, os
print("🔍 查找 npm 完整路径...")
# where 命令找 npm
res = subprocess.run(['where', 'npm'], capture_output=True, text=True)
if res.returncode == 0:
    print(f"找到 npm：\n{res.stdout}")
else:
    print("where 没找到，试试 where node 然后找 npm...")
    res_node = subprocess.run(['where', 'node'], capture_output=True, text=True)
    if res_node.returncode == 0:
        node_path = res_node.stdout.strip().split('\n')[0]
        node_dir = os.path.dirname(node_path)
        print(f"Node 目录：{node_dir}")
        npm_path = os.path.join(node_dir, 'npm.cmd')
        if os.path.exists(npm_path):
            print(f"✅ 找到 npm：{npm_path}")
        else:
            print(f"❌ npm 不存在于 node 目录")