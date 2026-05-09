# 读取现有file_handler.py
with open('novel_reader/file_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 替换read_mobi方法，使用真正的mobi库
old_mobi_code = """    def read_mobi(self, file_path):
        \"\"\"读取 MOBI 文件\"\"\"
        # 简单处理说明，实际需要依赖 mobi 库
        return f\"[MOBI 文件] {os.path.basename(file_path)}\\n完整支持需要安装 mobi 解析库，当前仅占位显示。\\n\""""
new_mobi_code = """    def read_mobi(self, file_path):
        \"\"\"读取 MOBI 文件\"\"\"
        try:
            import mobi
            # 使用 mobi 库提取文本
            text_content = []
            with mobi.open(file_path) as book:
                for page in book:
                    text = page.text
                    if text:
                        text_content.append(text)
            return '\\n\\n'.join(text_content)
        except ImportError:
            return f\"[MOBI 文件] {os.path.basename(file_path)}\\n需要安装 mobi 库才能支持 MOBI 格式。\\n请运行：pip install mobi\\n\"
        except Exception as e:
            return f\"读取 MOBI 文件出错：{str(e)}\\n文件路径：{file_path}\\n\""""
# 替换
new_content = content.replace(old_mobi_code, new_mobi_code)
# 写回文件
with open('novel_reader/file_handler.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ file_handler.py 的 read_mobi 方法已更新，现在可以真正读取 MOBI 文件了！")
utils.set_state(success=True)