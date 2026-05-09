with open('novel_reader/file_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()
print("当前file_handler.py内容：")
print(content)
utils.set_state(success=True, content=content)