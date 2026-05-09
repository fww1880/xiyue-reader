import os
import sys
# 读取当前 file_handler.py
handler_path = os.path.join(os.getcwd(), 'novel_reader', 'file_handler.py')
with open(handler_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修复 _convert_img_to_base64 —— 支持递归查找图片 + 添加自适应样式
old_method = """    def _convert_img_to_base64(self, soup, base_dir):
        \"\"\"将soup中的图片转换为base64，以便在QTextEdit中直接显示\"\"\"
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # 解析图片路径
                img_path = os.path.normpath(os.path.join(base_dir, src))
                if os.path.exists(img_path):
                    try:
                        with open(img_path, 'rb') as f:
                            data = f.read()
                            b64 = base64.b64encode(data).decode('utf-8')
                            # 设置MIME类型
                            ext = os.path.splitext(img_path)[1].lower()
                            mime = 'image/jpeg'
                            if ext == '.png': mime = 'image/png'
                            elif ext == '.gif': mime = 'image/gif'
                            elif ext == '.svg': mime = 'image/svg+xml'
                            # 替换src为base64
                            img['src'] = f\"data:{mime};base64,{b64}\"
                    except Exception:
                        pass # 转换失败则忽略"""
new_method = """    def _convert_img_to_base64(self, soup, base_dir):
        \"\"\"将soup中的图片转换为base64，以便在QTextEdit中直接显示\"
        支持递归查找图片文件，并添加自适应窗口样式\"\"\"
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # 添加自适应样式
                img['style'] = 'max-width:100%; height:auto;'
                # 解析图片路径
                img_path = os.path.normpath(os.path.join(base_dir, src))
                if not os.path.exists(img_path):
                    # 递归查找：可能在子目录中
                    for root, dirs, files in os.walk(base_dir):
                        for f in files:
                            if f == os.path.basename(src):
                                img_path = os.path.join(root, f)
                                break
                        if os.path.exists(img_path):
                            break
                if os.path.exists(img_path):
                    try:
                        with open(img_path, 'rb') as f:
                            data = f.read()
                            b64 = base64.b64encode(data).decode('utf-8')
                            # 设置MIME类型
                            ext = os.path.splitext(img_path)[1].lower()
                            mime = 'image/jpeg'
                            if ext == '.png': mime = 'image/png'
                            elif ext == '.gif': mime = 'image/gif'
                            elif ext == '.svg': mime = 'image/svg+xml'
                            # 替换src为base64
                            img['src'] = f\"data:{mime};base64,{b64}\"
                    except Exception:
                        pass # 转换失败则忽略"""
content = content.replace(old_method, new_method)
# 2. 修复 read_mobi —— 确保 base_dir 包含 Images 子目录
old_mobi = """    def read_mobi(self, file_path):
        \"\"\"读取MOBI文件，提取HTML并处理图片\"\"\"
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f\"[MOBI文件] {os.path.basename(file_path)}\\n文件提取失败\\n\"
            
            with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            # MOBI提取后，图片通常在 tempdir/Images，html在 tempdir
            # 所以 base_dir 设为 tempdir 即可解析相对路径
            self._convert_img_to_base64(soup, base_dir=tempdir)
            return str(soup)"""
new_mobi = """    def read_mobi(self, file_path):
        \"\"\"读取MOBI文件，提取HTML并处理图片\"\"\"
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f\"[MOBI文件] {os.path.basename(file_path)}\\n文件提取失败\\n\"
            
            with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            # MOBI提取后，图片可能在 tempdir/Images 或 tempdir/OEBPS/Images
            # 先尝试 html_path 所在目录，再尝试 tempdir
            self._convert_img_to_base64(soup, base_dir=os.path.dirname(html_path))
            # 如果图片还没找到，再尝试 tempdir
            self._convert_img_to_base64(soup, base_dir=tempdir)
            return str(soup)"""
content = content.replace(old_mobi, new_mobi)
# 写入文件
with open(handler_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("file_handler.py 已修复完成！")
print("修复内容：")
print("1. _convert_img_to_base64: 支持递归查找图片 + 添加 max-width:100% 自适应样式")
print("2. read_mobi: 增加 base_dir 为 html_path 所在目录")