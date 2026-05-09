import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查看 init_ui 中书架面板的布局
start = content.find('def init_ui')
end = content.find('\n    def create_menu_bar', start)
print("📄 init_ui 方法：")
print(content[start:end])
print("\n" + "="*50)
# 查看 load_book 方法
start2 = content.find('def load_book')
end2 = content.find('\n    def build_table_of_contents', start2)
print("\n📄 load_book 方法：")
print(content[start2:end2])