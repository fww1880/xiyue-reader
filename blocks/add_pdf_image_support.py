import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 替换 load_book 方法开头，增加 PDF 判断
old_start = '''    def load_book(self, file_path):
        """加载书籍文件"""
        try:
            from file_handler import FileHandler
            handler = FileHandler()
            content = handler.read_file(file_path)
            # 智能识别内容类型：如果是HTML则使用富文本显示，支持图片
            is_html = False
            stripped = content.strip()
            if stripped.startswith('<html') or stripped.startswith('<!DOCTYPE') or '<img' in stripped:
                is_html = True
            if is_html:
                self.text_edit.setHtml(content)
            else:
                self.text_edit.setPlainText(content)
            self.current_book_path = file_path'''
new_start = '''    def load_book(self, file_path):
        """加载书籍文件"""
        try:
            self.current_book_path = file_path
            self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")
            
            # 判断是否为 PDF 文件，使用图片分页模式打开
            if file_path.lower().endswith('.pdf'):
                self.load_pdf_as_images(file_path)
                return
            from file_handler import FileHandler
            handler = FileHandler()
            content = handler.read_file(file_path)
            # 智能识别内容类型：如果是HTML则使用富文本显示，支持图片
            is_html = False
            stripped = content.strip()
            if stripped.startswith('<html') or stripped.startswith('<!DOCTYPE') or '<img' in stripped:
                is_html = True
            if is_html:
                self.text_edit.setHtml(content)
            else:
                self.text_edit.setPlainText(content)'''
if old_start in content:
    content = content.replace(old_start, new_start)
    print("✅ 已更新 load_book 方法开头，增加 PDF 分支")
else:
    print("⚠️ 未找到 load_book 开头代码")
# 2. 插入 load_pdf_as_images 方法
# 找到 load_book 结束的位置（即下一个 def 开始）
pattern = r'(    def load_book\(self, file_path\):.*?)(\n    def \w+)'
match = re.search(pattern, content, re.DOTALL)
if match:
    load_book_part = match.group(1)
    next_def_part = match.group(2)
    
    new_method = '''
    def load_pdf_as_images(self, file_path):
        """将 PDF 渲染为图片并分页显示，保留原格式"""
        try:
            import fitz # PyMuPDF
            from PyQt5.QtGui import QImage, QPixmap
            from PyQt5.QtCore import Qt
            
            self.text_edit.clear()
            self.text_edit.setReadOnly(True) # PDF 模式下设为只读
            
            doc = fitz.open(file_path)
            cursor = self.text_edit.textCursor()
            
            # 设置缩放比例，2.0 比较清晰
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=mat)
                
                # 转换为 QImage
                img_data = pix.tobytes("png")
                qimage = QImage.fromData(img_data)
                
                if qimage.isNull():
                    continue
                    
                pixmap = QPixmap.fromImage(qimage)
                
                # 插入图片
                cursor.insertImage(pixmap.toImage())
                cursor.insertText("\\n") # 分页间隔
                
            doc.close()
            self.status_bar.showMessage(f"✅ PDF 加载完成，共 {len(doc)} 页", 3000)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载 PDF 失败：{str(e)}")
'''
    content = content.replace(match.group(0), load_book_part + new_method + next_def_part)
    print("✅ 已添加 load_pdf_as_images 方法")
else:
    print("❌ 未找到插入点")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
    
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e}")