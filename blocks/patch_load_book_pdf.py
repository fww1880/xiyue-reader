import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 load_book 的精确位置
old_try = '''    def load_book(self, file_path):
        """加载书籍文件"""
        try:
            from file_handler import FileHandler'''
new_try = '''    def load_book(self, file_path):
        """加载书籍文件"""
        try:
            self.current_book_path = file_path
            self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")
            
            # 判断是否为 PDF 文件，使用图片分页模式打开
            if file_path.lower().endswith('.pdf'):
                self.load_pdf_as_images(file_path)
                return
                
            from file_handler import FileHandler'''
if old_try in content:
    content = content.replace(old_try, new_try)
    print("✅ 已修补 load_book，增加了 PDF 分支判断")
else:
    print("⚠️ 未找到精确匹配，尝试模糊匹配...")
    # 备用方案：查找 def load_book 并在下一行 try: 后插入
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def load_book(self, file_path):' in line:
            # 找到 try: 行
            for j in range(i, i+5):
                if 'try:' in lines[j]:
                    indent = '            '
                    new_lines = [
                        f'{indent}self.current_book_path = file_path',
                        f'{indent}self.setWindowTitle(f"喜阅 - {{os.path.basename(file_path)}}")',
                        f'{indent}if file_path.lower().endswith(".pdf"):',
                        f'{indent}    self.load_pdf_as_images(file_path)',
                        f'{indent}    return',
                        ''
                    ]
                    # 插入到 try: 之后
                    for k, nl in enumerate(new_lines):
                        lines.insert(j + 1 + k, nl)
                    print(f"✅ 已在第 {j+1} 行后插入 PDF 判断逻辑")
                    break
            break
    content = '\n'.join(lines)
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