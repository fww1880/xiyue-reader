import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 去掉工具栏按钮 QToolButton 的边框（L526）
old_toolbutton = """QToolButton {
background-color: #FFFFFF;
border: 2px solid #AEC6CF; /* 马卡龙蓝边框 */
border-radius: 12px;
padding: 8px 14px;
color: #555555;
font-size: 14px; /* 字体加大 */
font-weight: bold;
font-family: "Microsoft YaHei";
}
QToolButton:hover {
background-color: #FDFD96; /* 马卡龙黄悬停 */
border-color: #FFB7B2;
}
QToolButton:pressed {
background-color: #77DD77; /* 马卡龙绿按下 */
border-color: #C3B1E1;
}
QToolButton:checked {
background-color: #FFB7B2; /* 选中状态 (马卡龙粉) */
color: white;
border-color: #FF6961;
}"""
new_toolbutton = """QToolButton {
background-color: #E3F2FD; /* 浅蓝背景 */
border: none; /* 无边框 */
border-radius: 12px;
padding: 8px 14px;
color: #1976D2; /* 深蓝色文字 */
font-size: 14px; /* 字体加大 */
font-weight: bold;
font-family: "Microsoft YaHei";
}
QToolButton:hover {
background-color: #BBDEFB; /* 浅蓝悬停 */
}
QToolButton:pressed {
background-color: #64B5F6; /* 深蓝按下 */
color: white;
}
QToolButton:checked {
background-color: #64B5F6; /* 蓝色选中 */
color: white;
}"""
content = content.replace(old_toolbutton, new_toolbutton)
# 2. 在书架样式后添加 QListWidget 无边框样式
old_bookshelf_style = """QDockWidget::close-button, QDockWidget::float-button {
border: none;
background: none;
}
"""
new_bookshelf_style = """QDockWidget::close-button, QDockWidget::float-button {
border: none;
background: none;
}
/* 目录和书签列表框 - 无边框浅蓝色 */
QListWidget {
background-color: #F5F9FC;
border: none;
outline: none;
}
QListWidget::item:selected {
background-color: #BBDEFB;
}
QListWidget::item:hover {
background-color: #E3F2FD;
}
"""
content = content.replace(old_bookshelf_style, new_bookshelf_style)
# 3. bm_label 和 toc_label 也改成蓝色风格
old_bm_label = 'self.bm_label.setStyleSheet("font-weight: bold; color: #555;")'
new_bm_label = 'self.bm_label.setStyleSheet("font-weight: bold; color: #1976D2; background-color: #E3F2FD; padding: 4px; border-radius: 3px;")'
content = content.replace(old_bm_label, new_bm_label)
old_toc_label = 'self.toc_label.setStyleSheet("font-weight: bold; padding: 3px; background-color: #e0e0e0; border-radius: 3px;")'
new_toc_label = 'self.toc_label.setStyleSheet("font-weight: bold; color: #1976D2; background-color: #E3F2FD; padding: 4px; border-radius: 3px; border: none;")'
content = content.replace(old_toc_label, new_toc_label)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 已完成：")
print("  1. 工具栏按钮去掉边框，改为浅蓝背景+深蓝色文字")
print("  2. 目录和书签列表框 → 淡蓝色背景，无边框，选中高亮浅蓝")
print("  3. 目录/书签标签 → 蓝色调背景文字")
print("所有黑色边框/黑底全部清理完毕！")