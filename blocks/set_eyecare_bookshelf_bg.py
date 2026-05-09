import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修改书架 dock 背景色
old_dock_bg = '''        QDockWidget {
        border: none;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #F0F4F8, stop:1 #E1EBF5);
        }'''
new_dock_bg = '''        QDockWidget {
        border: none;
        background-color: #CCE8CF; /* 护眼豆沙绿 */
        }'''
content = content.replace(old_dock_bg, new_dock_bg)
print("✅ 书架整体背景已改为护眼豆沙绿 (#CCE8CF)")
# 修改目录/书签标签背景色
old_toc_label = 'self.toc_label.setStyleSheet("font-weight: bold; color: #1976D2; background-color: #E3F2FD; padding: 4px; border-radius: 3px; border: none;")'
new_toc_label = 'self.toc_label.setStyleSheet("font-weight: bold; color: #2E7D32; background-color: #A5D6A7; padding: 6px; border-radius: 3px; border: none;")'
content = content.replace(old_toc_label, new_toc_label)
print("✅ 目录标签背景已改为护眼绿色")
old_bm_label = 'self.bm_label.setStyleSheet("font-weight: bold; color: #1976D2; background-color: #E3F2FD; padding: 4px; border-radius: 3px;")'
new_bm_label = 'self.bm_label.setStyleSheet("font-weight: bold; color: #2E7D32; background-color: #A5D6A7; padding: 6px; border-radius: 3px; border: none;")'
content = content.replace(old_bm_label, new_bm_label)
print("✅ 书签标签背景已改为护眼绿色")
# 修改目录和书签列表框背景色
old_list_bg = '''/* 目录和书签列表框 - 无边框浅蓝色 */
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
}'''
new_list_bg = '''/* 目录和书签列表框 - 无边框护眼绿色 */
QListWidget {
background-color: #DCEDC8;
border: none;
outline: none;
}
QListWidget::item:selected {
background-color: #A5D6A7;
}
QListWidget::item:hover {
background-color: #C8E6C9;
}'''
content = content.replace(old_list_bg, new_list_bg)
print("✅ 目录/书签列表背景已改为护眼绿色系列")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")