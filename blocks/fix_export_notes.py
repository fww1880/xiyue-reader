import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 删除或注释掉引用 export_notes 的行
old_export = '''        export_notes_action = QAction("导出书签/笔记", self)
        export_notes_action.triggered.connect(self.export_notes)
        tool_menu.addAction(export_notes_action)'''
new_export = '''        # 导出书签功能已移除（集成到书架面板）'''
content = content.replace(old_export, new_export)
print("✅ 已移除 export_notes 引用")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("🚀 修复完成！")