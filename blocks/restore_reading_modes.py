import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查是否已有阅读模式按钮
if '白天' in content and '夜间' in content and '护眼' in content:
    print("✅ 阅读模式按钮已存在")
else:
    print("⚠️ 需要添加阅读模式按钮")
# 查找工具栏样式定义的位置
if 'macaron_css' in content:
    print("✅ 找到工具栏样式定义")
# 查找设置正文背景的方法
if 'set_text_background' in content or 'background_color' in content:
    print("✅ 找到背景设置相关代码")
else:
    print("需要添加背景切换方法")
print("\n开始分析如何恢复三种模式...")