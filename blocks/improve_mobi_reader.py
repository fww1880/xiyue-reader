# 读取现有file_handler.py
with open('novel_reader/file_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 改进read_mobi方法，让它能处理HTML内容
old_mobi_code = """    def read_mobi(self, file_path):
        \"\"\"读取MOBI文件\"\"\"
        try:
            import mobi
            # mobi库的正确用法：extract函数提取文本
            tempdir, file_path_extracted = mobi.extract(file_path)
            
            # 读取提取出来的文件内容
            if file_path_extracted and os.path.exists(file_path_extracted):
                # 提取出来的可能是epub文件
                ext = os.path.splitext(file_path_extracted)[1].lower()
                if ext == '.epub':
                    content = self.read_epub(file_path_extracted)
                else:
                    # 尝试按文本读取
                    with open(file_path_extracted, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                return content
            else:
                return f\"[MOBI文件] {os.path.basename(file_path)}\n文件提取失败，可能已损坏\n\"
        except ImportError:
            return f\"[MOBI文件] {os.path.basename(file_path)}\n需要安装 mobi 库才能支持MOBI格式。\n\"
        except Exception as e:
            return f\"读取MOBI文件出错：{str(e)}\n文件路径：{file_path}\n\""""
new_mobi_code = """    def read_mobi(self, file_path):
        \"\"\"读取MOBI文件\"\"\"
        try:
            import mobi
            # mobi库的正确用法：extract函数提取文本
            tempdir, file_path_extracted = mobi.extract(file_path)
            
            # 读取提取出来的文件内容
            if file_path_extracted and os.path.exists(file_path_extracted):
                # 提取出来的可能是epub文件
                ext = os.path.splitext(file_path_extracted)[1].lower()
                if ext == '.epub':
                    content = self.read_epub(file_path_extracted)
                else:
                    # 尝试按文本读取
                    with open(file_path_extracted, 'r', encoding='utf-8', errors='replace') as f:
                        html_content = f.read()
                    # 处理HTML内容，提取文本
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html_content, 'html.parser')
                        # 移除图片标签
                        for img_tag in soup.find_all('img'):
                            img_tag.decompose()
                        # 提取所有文本段落
                        text_content = []
                        paragraphs = soup.find_all('p')
                        for p in paragraphs:
                            text = p.get_text().strip()
                            if text:
                                text_content.append(text)
                        if text_content:
                            content = '\\n\\n'.join(text_content)
                        else:
                            # 如果没有段落标签，提取所有文本
                            content = soup.get_text().strip()
                    except ImportError:
                        # 如果没有BeautifulSoup，简单处理HTML
                        import re
                        # 移除HTML标签
                        content = re.sub(r'<[^>]+>', '', html_content)
                return content
            else:
                return f\"[MOBI文件] {os.path.basename(file_path)}\n文件提取失败，可能已损坏\n\"
        except ImportError:
            return f\"[MOBI文件] {os.path.basename(file_path)}\n需要安装 mobi 库才能支持MOBI格式。\n\"
        except Exception as e:
            return f\"读取MOBI文件出错：{str(e)}\n文件路径：{file_path}\n\""""
# 替换
new_content = content.replace(old_mobi_code, new_mobi_code)
# 写回文件
with open('novel_reader/file_handler.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ file_handler.py 的 read_mobi 方法已改进，现在能处理HTML内容并跳过图片了！")
utils.set_state(success=True)