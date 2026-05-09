import os
main_path = os.path.join(os.getcwd(), 'novel_reader', 'main.py')
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 load_book 方法
start = content.find('def load_book')
end = content.find('\n    def ', start + 10)
if end == -1:
    end = content.find('\nclass ', start + 10)
print("=== load_book 方法 ===")
print(content[start:end])
print("\n\n=== 文本显示组件 ===")
# 找到 QTextEdit 相关代码
text_edit_start = content.find('QTextEdit')
text_edit_end = content.find('\n        ', text_edit_start + 100)
print(content[max(0,text_edit_start-200):text_edit_end+200])