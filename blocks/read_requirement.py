# 读取需求文件内容
requirement_path = r"E:\AiPyPro\fww\阅读器要求.txt"
try:
    with open(requirement_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print("成功读取阅读器需求文件：\n")
    print(content)
    utils.set_state(success=True, content=content)
except Exception as e:
    try:
        with open(requirement_path, 'r', encoding='gbk') as f:
            content = f.read()
        print("成功用GBK编码读取阅读器需求文件：\n")
        print(content)
        utils.set_state(success=True, content=content)
    except Exception as e2:
        error_msg = f"读取文件失败，UTF-8错误: {str(e)}，GBK错误: {str(e2)}"
        print(error_msg)
        utils.set_state(success=False, error=error_msg)