# 读取现有file_handler.py
with open('novel_reader/file_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 替换read_mobi方法，使用正确的mobi.extract
old_mobi_code = """    def read_mobi(self, file_path):
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
new_mobi_code = """    def read_mobi(self, file_path):
        \"\"\"读取 MOBI 文件\"\"\"
        try:
            import mobi
            # mobi库的正确用法：extract函数提取文本
            tempdir, epub_path = mobi.extract(file_path)
            
            # 读取提取出来的EPUB内容
            if epub_path:
                # 临时使用read_epub方法来读取提取出来的EPUB
                return self.read_epub(epub_path)
            else:
                return f\"[MOBI 文件] {os.path.basename(file_path)}\\n文件提取失败\\n\"
        except ImportError:
            return f\"[MOBI 文件] {os.path.basename(file_path)}\\n需要安装 mobi 库才能支持 MOBI 格式。\\n\"
        except Exception as e:
            return f\"读取 MOBI 文件出错：{str(e)}\\n文件路径：{file_path}\\n\""""
# 替换
new_content = content.replace(old_mobi_code, new_mobi_code)
# 写回文件
with open('novel_reader/file_handler.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ file_handler.py 的 read_mobi 方法已修复，现在使用正确的 mobi.extract 方法！")
utils.set_state(success=True)