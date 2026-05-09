import os
# 列出当前目录所有文件
print("当前目录文件：")
for file in os.listdir('.'):
    print(f"  {file}")
# 看看blocks目录
print("\nblocks目录文件：")
if os.path.exists('blocks'):
    for file in os.listdir('blocks'):
        if file.endswith('.py'):
            print(f"  {file}")
utils.set_state(success=True)