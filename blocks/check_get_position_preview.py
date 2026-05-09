import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查 get_position_preview 方法
start = content.find('def get_position_preview')
if start != -1:
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    method = content[start:end]
    print("✅ get_position_preview 方法存在：")
    print(method)
else:
    print("❌ get_position_preview 方法不存在！需要添加")
    # 添加这个方法
    # 找到 add_bookmark 方法之前插入
    add_bm_pos = content.find('def add_bookmark')
    if add_bm_pos != -1:
        new_method = '''
    def get_position_preview(self, pos):
        """获取位置附近的文本预览"""
        cursor = self.text_edit.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.StartOfBlock)
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        preview = cursor.selectedText().strip()
        if len(preview) > 50:
            preview = preview[:50]
        return preview if preview else "位置 " + str(pos)
'''
        content = content[:add_bm_pos] + new_method + content[add_bm_pos:]
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 已添加 get_position_preview 方法")