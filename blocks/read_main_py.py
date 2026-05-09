# 读取main.py代码
with open('novel_reader/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
print("main.py代码内容：\n")
print(content)
utils.set_state(success=True, content=content)