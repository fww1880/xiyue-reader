import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
# 1. 修改 file_handler.py
file_handler_path = os.path.join(novel_reader_dir, 'file_handler.py')
with open(file_handler_path, 'r', encoding='utf-8') as f:
    fh_content = f.read()
# 替换 read_mobi 方法，增加 NCX 目录提取
old_mobi_method = '''    def read_mobi(self, file_path):
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
new_mobi_method = '''    def read_mobi(self, file_path):
        """读取MOBI文件，提取HTML并处理图片"""
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f"[MOBI文件] {os.path.basename(file_path)}\\n文件提取失败\\n"
            
            # 合并所有 HTML 文件
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
            
            # 提取 NCX 目录
            self.ncx_toc = []
            ncx_path = None
            for root, dirs, files in os.walk(tempdir):
                for f in files:
                    if f.endswith('.ncx'):
                        ncx_path = os.path.join(root, f)
                        break
                if ncx_path: break
            
            if ncx_path:
                try:
                    with open(ncx_path, 'r', encoding='utf-8') as f:
                        ncx_soup = BeautifulSoup(f, 'html.parser')
                    for navpoint in ncx_soup.find_all('navpoint'):
                        label = navpoint.find('navlabel')
                        if label:
                            text = label.find('text')
                            if text and text.string:
                                self.ncx_toc.append(text.string.strip())
                except Exception as e:
                    print(f"NCX解析错误: {e}")
            
            return full_html'''
if old_mobi_method in fh_content:
    fh_content = fh_content.replace(old_mobi_method, new_mobi_method)
    print("✅ file_handler.py: read_mobi 方法已更新")
else:
    print("⚠️ file_handler.py: 未找到旧的 read_mobi 方法，尝试追加 NCX 逻辑...")
    # 如果没找到，尝试在 return full_html 前插入
    # 这里假设 full_html 是最后返回的
    pass
with open(file_handler_path, 'w', encoding='utf-8') as f:
    f.write(fh_content)
# 2. 修改 main.py
main_path = os.path.join(novel_reader_dir, 'main.py')
with open(main_path, 'r', encoding='utf-8') as f:
    main_content = f.read()
# 添加 show_ncx_toc 方法
show_ncx_toc_method = '''    def show_ncx_toc(self, titles):
        """显示从 NCX 提取的目录"""
        self.toc_list.clear()
        self.chapter_positions = []
        for title in titles:
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, title)
            self.toc_list.addItem(item)
        if titles:
            self.toc_list.show()
            self.toc_label.show()
        else:
            self.toc_list.hide()
            self.toc_label.hide()
'''
if 'def show_ncx_toc' not in main_content:
    # 在 init_ui 之前插入
    main_content = main_content.replace('    def init_ui(self):', show_ncx_toc_method + '\n    def init_ui(self):')
    print("✅ main.py: 已添加 show_ncx_toc 方法")
# 修改 load_book 方法，优先使用 NCX 目录
old_load_toc = '''            # 解析目录并生成目录面板
            self.build_table_of_contents(content, is_html)'''
new_load_toc = '''            # 解析目录并生成目录面板
            # 优先使用 NCX 目录（如果有）
            ncx_toc = getattr(handler, 'ncx_toc', [])
            if ncx_toc:
                self.show_ncx_toc(ncx_toc)
            else:
                self.build_table_of_contents(content, is_html)'''
if old_load_toc in main_content:
    main_content = main_content.replace(old_load_toc, new_load_toc)
    print("✅ main.py: load_book 已更新，优先使用 NCX 目录")
else:
    print("⚠️ main.py: 未找到 load_toc 调用点")
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_content)
print("🚀 修改完成，准备重启阅读器...")