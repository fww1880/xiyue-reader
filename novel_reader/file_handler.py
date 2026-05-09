import os
import chardet
import base64
import zipfile
import tempfile
from bs4 import BeautifulSoup
class FileHandler:
    """文件处理工具类，处理不同格式的小说文件读取"""
    
    def __init__(self):
        self.supported_formats = ['.txt', '.epub', '.mobi', '.pdf']
        
    def detect_encoding(self, file_path):
        """检测文件编码"""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            return result['encoding']
        
    def _convert_img_to_base64(self, soup, base_dir):
        """将soup中的图片转换为base64，以便在QTextEdit中直接显示"
        支持递归查找图片文件，并添加自适应窗口样式"""
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
                            img['src'] = f"data:{mime};base64,{b64}"
                    except Exception:
                        pass # 转换失败则忽略
    def read_txt(self, file_path):
        """读取TXT文件"""
        try:
            encoding = self.detect_encoding(file_path)
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            return f.read()
                    except UnicodeDecodeError:
                        continue
            raise Exception(f"无法解码文件 {file_path}")
        except Exception as e:
            raise Exception(f"读取TXT文件失败：{str(e)}")
        
    def read_epub(self, file_path):
        """读取EPUB文件，提取HTML内容并处理图片"""
        try:
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.extractall(temp_dir)
            
            # 查找所有html文件
            html_files = []
            for root, dirs, files in os.walk(temp_dir):
                for f in files:
                    if f.endswith(('.html', '.xhtml')):
                        html_files.append(os.path.join(root, f))
            # 排序以保证阅读顺序
            html_files.sort()
            
            full_html = "<html><body>"
            for h_file in html_files:
                with open(h_file, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                # 处理图片，base_dir为当前html文件所在目录
                self._convert_img_to_base64(soup, base_dir=os.path.dirname(h_file))
                
                if soup.body:
                    full_html += str(soup.body) + "<br/>"
                else:
                    full_html += str(soup) + "<br/>"
            full_html += "</body></html>"
            return full_html
        except Exception as e:
            return f"读取EPUB出错：{str(e)}"
        
    def read_mobi(self, file_path):
        """读取MOBI文件，提取HTML并处理图片"""
        try:
            import mobi
            tempdir, html_path = mobi.extract(file_path)
            
            if not html_path or not os.path.exists(html_path):
                return f"[MOBI文件] {os.path.basename(file_path)}\n文件提取失败\n"
            
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
            
            return full_html
        except ImportError:
            return f"[MOBI文件] {os.path.basename(file_path)}\n需要安装 mobi 库才能支持MOBI格式。\n"
        except Exception as e:
            return f"读取MOBI文件出错：{str(e)}\n文件路径：{file_path}\n"
        
    def read_pdf(self, file_path):
        """读取PDF文件"""
        try:
            from PyPDF2 import PdfReader
            if not os.path.exists(file_path):
                return f"错误：PDF文件不存在\n"
            
            reader = PdfReader(file_path)
            if reader.is_encrypted:
                return f"错误：PDF文件已加密，无法读取\n"
            
            text_content = []
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                except:
                    continue
                    
            if not text_content:
                return f"警告：PDF文件可能没有文本内容或格式特殊\n"
            return '\n\n'.join(text_content)
        except ImportError:
            return "错误：需要安装 PyPDF2 库才能支持PDF格式\n"
        except Exception as e:
            return f"读取PDF文件出错：{str(e)}\n"
        
    def _demo_content(self, file_path):
        return f"\n文件路径: {file_path}\n请检查文件是否损坏或安装对应依赖库以支持此格式。"
        
    def read_file(self, file_path):
        """根据文件扩展名选择读取方式"""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.txt':
                return self.read_txt(file_path)
            elif ext == '.epub':
                return self.read_epub(file_path)
            elif ext == '.mobi':
                return self.read_mobi(file_path)
            elif ext == '.pdf':
                return self.read_pdf(file_path)
            else:
                return self.read_txt(file_path)
        except Exception as e:
            return f"读取文件失败：{str(e)}"