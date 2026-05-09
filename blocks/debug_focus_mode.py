import os
novel_reader_dir = os.getcwd() + '\\novel_reader'
main_file = novel_reader_dir + '\\main.py'
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 toggle_focus_mode 方法
start = content.find('def toggle_focus_mode')
if start == -1:
    print("❌ 未找到 toggle_focus_mode 方法")
else:
    end = content.find('\n    def ', start + 1)
    if end == -1: end = len(content)
    print("📄 toggle_focus_mode 方法内容：")
    print(content[start:end])
# 检查 init_ui 中书架面板的定义
if 'self.bookshelf_panel' in content:
    print("\n⚠️ 发现旧代码引用 self.bookshelf_panel（浮动窗口改造后应使用 self.bookshelf_dock）")
else:
    print("\n✅ 未发现旧的 bookshelf_panel 引用")