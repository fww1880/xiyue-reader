import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找现有的翻页相关功能
print("🔍 查找现有的翻页功能...")
# 查找键盘快捷键绑定
keyboard_start = content.find('keyboard_action')
keyboard_end = content.find('\n    def ', keyboard_start)
if keyboard_end == -1:
    keyboard_end = len(content)
print("📋 键盘快捷键绑定：")
print(content[keyboard_start:keyboard_end])
# 查找鼠标滚轮处理
mouse_start = content.find('wheel_event')
mouse_end = content.find('\n    def ', mouse_start)
if mouse_end == -1:
    mouse_end = len(content)
print("\n📋 鼠标滚轮处理：")
print(content[mouse_start:mouse_end])
# 查找自动滚屏
auto_start = content.find('auto_scroll')
auto_end = content.find('\n    def ', auto_start)
if auto_end == -1:
    auto_end = len(content)
print("\n📋 自动滚屏相关：")
print(content[auto_start:auto_end])