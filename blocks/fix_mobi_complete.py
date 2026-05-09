import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
# ===== 1. 修复 file_handler.py - MOBI 合并所有 HTML 片段 =====
file_handler = os.path.join(novel_reader_dir, 'file_handler.py')
with open(file_handler, 'r', encoding='utf-8') as f:
    fh_content = f.read()
old_mobi = '''    def read_mobi(self, file_path):
        """读取MOBI文件，提取HTML并处理图片"""
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f"[MOBI文件] {os.path.basename(file_path)}\\n文件提取失败\\n"
            
            with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            # MOBI提取后，图片可能在 tempdir/Images 或 tempdir/OEBPS/Images
            # 先尝试 html_path 所在目录，再尝试 tempdir
            self._convert_img_to_base64(soup, base_dir=os.path.dirname(html_path))
            # 如果图片还没找到，再尝试 tempdir
            self._convert_img_to_base64(soup, base_dir=tempdir)
            return str(soup)'''
new_mobi = '''    def read_mobi(self, file_path):
        """读取MOBI文件，提取HTML并处理图片"""
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f"[MOBI文件] {os.path.basename(file_path)}\\n文件提取失败\\n"
            
            # 合并所有 HTML 文件，确保目录和内容完整
            html_files = []
            for root, dirs, files in os.walk(tempdir):
                for f in files:
                    if f.endswith(('.html', '.xhtml')):
                        html_files.append(os.path.join(root, f))
            html_files.sort()
            
            full_html = "<html><body>"
            for h_file in html_files:
                with open(h_file, 'r', encoding='utf-8', errors='replace') as f:
                    h_content = f.read()
                soup = BeautifulSoup(h_content, 'html.parser')
                self._convert_img_to_base64(soup, base_dir=os.path.dirname(h_file))
                if soup.body:
                    full_html += str(soup.body) + "<br/>"
                else:
                    full_html += str(soup) + "<br/>"
            full_html += "</body></html>"
            
            return full_html'''
fh_content = fh_content.replace(old_mobi, new_mobi)
with open(file_handler, 'w', encoding='utf-8') as f:
    f.write(fh_content)
print("✅ file_handler.py 修复：MOBI 现在合并所有 HTML 片段")
# ===== 2. 修复 main.py - 正则表达式转义错误 =====
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    main_content = f.read()
# 修复正则表达式中的转义（之前多了反斜杠）
main_content = main_content.replace(r'^\\s*(第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]', r'^\s*(第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集]')
main_content = main_content.replace(r'Chapter\\s+[0-9IVXLCDM]+', r'Chapter\s+[0-9IVXLCDM]+')
main_content = main_content.replace(r'Part\\s+[0-9IVXLCDM]+', r'Part\s+[0-9IVXLCDM]+')
main_content = main_content.replace(r'^\\s*第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]\\s*.*$', r'^\s*第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集]\s*.*$')
main_content = main_content.replace(r'^\\s*Chapter\\s+[0-9IVXLCDM]+[.:、\\s].*$', r'^\s*Chapter\s+[0-9IVXLCDM]+[.:、\s].*$')
main_content = main_content.replace(r'^\\s*Part\\s+[0-9IVXLCDM]+[.:、\\s].*$', r'^\s*Part\s+[0-9IVXLCDM]+[.:、\s].*$')
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(main_content)
print("✅ main.py 修复：正则表达式转义已修正")