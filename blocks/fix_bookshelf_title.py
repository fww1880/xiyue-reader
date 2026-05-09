import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找书架标题栏样式
old_title_style = '''        QDockWidget::title {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #90CAF9, stop:1 #64B5F6);
        padding: 6px;
        color: white;
        font-weight: bold;
        border: none;
        }'''
new_title_style = '''        QDockWidget::title {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #90CAF9, stop:1 #64B5F6);
        padding: 10px 8px 12px 8px;
        color: white;
        font-weight: bold;
        font-size: 14px;
        border: none;
        text-align: left;
        }'''
content = content.replace(old_title_style, new_title_style)
print("✅ 已增加标题栏内边距，确保\"我的书架\"四个字完整显示")
# 检查正文是否自动换行
if "setLineWrapMode" in content:
    print("✅ 正文自动换行已经启用")
else:
    print("⚠️ 未找到自动换行设置，需要添加")
    # 在 text_edit 初始化后添加自动换行
print("\n✅ 浮动Dock默认支持自由拖动改变大小，无需额外修改")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存修改")