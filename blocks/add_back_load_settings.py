import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 在 __init__ 中 load_settings 被引用但方法不存在，添加它
# 找到 __init__ 中 self.load_settings() 的位置
pos = content.find('self.load_settings()')
if pos != -1:
    # 在 __init__ 之后插入 load_settings 方法
    init_end = content.find('\n    def ', content.find('def __init__') + 1)
    load_settings_method = '''
    def load_settings(self):
        """加载设置"""
        self.settings = QSettings('NovelReader', 'Settings')
        self.font_size = self.settings.value('font_size', 16, int)
        self.line_spacing = self.settings.value('line_spacing', 1.5, float)
        self.theme = self.settings.value('theme', 'light', str)
        self.auto_scroll_speed = self.settings.value('auto_scroll_speed', 30, int)
'''
    content = content[:init_end] + load_settings_method + content[init_end:]
    print("✅ 已添加 load_settings 方法")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)