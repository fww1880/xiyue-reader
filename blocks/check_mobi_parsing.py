import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查看 build_table_of_contents 中 HTML 部分的解析逻辑
start = content.find('def build_table_of_contents')
end = content.find('\n    def jump_to_chapter', start)
if end == -1:
    end = len(content)
    
print("📄 build_table_of_contents 方法（HTML部分）：")
method_content = content[start:end]
# 提取 HTML 处理部分
html_part_start = method_content.find('if is_html:')
html_part_end = method_content.find('else:', html_part_start)
print(method_content[html_part_start:html_part_end])