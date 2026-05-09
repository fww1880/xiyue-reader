# 读取现有file_handler.py
with open('novel_reader/file_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 优化read_pdf方法，增加更多异常处理
old_pdf_code = """    def read_pdf(self, file_path):
        \"\"\"读取 PDF 文件\"\"\"
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            # 检查是否加密
            if reader.is_encrypted:
                return f\"错误：PDF 文件已加密，无法读取\\n{self._demo_content(file_path)}\"
            
            text_content = []
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                except Exception as page_error:
                    # 单页读取失败，跳过继续
                    continue
                    
            return '\\n\\n'.join(text_content)
        except ImportError:
            return \"错误：需要安装 PyPDF2 库才能支持 PDF 格式\\n\" + self._demo_content(file_path)
        except Exception as e:
            return f\"读取 PDF 文件出错：{str(e)}\\n\" + self._demo_content(file_path)"""
new_pdf_code = """    def read_pdf(self, file_path):
        \"\"\"读取 PDF 文件\"\"\"
        try:
            from PyPDF2 import PdfReader
            
            # 先检查文件是否存在
            if not os.path.exists(file_path):
                return f\"错误：PDF 文件不存在\\n文件路径：{file_path}\\n\"
            
            reader = PdfReader(file_path)
            # 检查是否加密
            if reader.is_encrypted:
                return f\"错误：PDF 文件已加密，无法读取\\n{self._demo_content(file_path)}\"
            
            text_content = []
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                except Exception as page_error:
                    # 单页读取失败，跳过继续
                    continue
                    
            if not text_content:
                return f\"警告：PDF 文件可能没有文本内容或格式特殊\\n{self._demo_content(file_path)}\"
                    
            return '\\n\\n'.join(text_content)
        except ImportError:
            return \"错误：需要安装 PyPDF2 库才能支持 PDF 格式\\n\" + self._demo_content(file_path)
        except Exception as e:
            return f\"读取 PDF 文件出错：{str(e)}\\n\" + self._demo_content(file_path)"""
# 替换
new_content = content.replace(old_pdf_code, new_pdf_code)
# 写回文件
with open('novel_reader/file_handler.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ file_handler.py 的 read_pdf 方法已优化，增加了文件检查和空内容处理！")
utils.set_state(success=True)