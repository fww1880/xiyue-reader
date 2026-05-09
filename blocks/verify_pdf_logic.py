import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查 load_book 是否调用了 load_pdf_as_images
if 'self.load_pdf_as_images' in content:
    # 找到 load_book 定义
    idx = content.find('def load_book(self, file_path):')
    if idx != -1:
        # 截取 load_book 的前 500 个字符
        block = content[idx:idx+500]
        if 'load_pdf_as_images' in block:
            print("✅ 验证通过：load_book 中已包含 PDF 调用逻辑")
        else:
            print("❌ 验证失败：load_pdf_as_images 方法存在，但未被 load_book 调用")
    else:
        print("❌ 未找到 load_book 方法")
else:
    print("❌ 未找到 load_pdf_as_images 调用")