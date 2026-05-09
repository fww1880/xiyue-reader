# 读取main.py文件看看哪里有问题
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()
print(content)
utils.set_state(success=True, result=content)