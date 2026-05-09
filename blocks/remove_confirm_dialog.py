import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找并移除确认对话框代码
# 原逻辑：先弹出对话框询问，用户确认后调用 add_bookmark
# 新逻辑：直接调用 add_bookmark
old_code = '''        # 显示确认对话框
        reply = QMessageBox.question(
            self, '确认添加', 
            f'确定要添加书签吗？\\n位置：{self.current_chapter} - {pos_text}',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.add_bookmark()'''
new_code = '''        # 直接添加书签，无需确认
        self.add_bookmark()'''
if old_code in content:
    content = content.replace(old_code, new_code)
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已移除确认弹窗，现在添加书签无需确认！")
else:
    # 尝试另一种可能的写法
    old_code_v2 = '''reply = QMessageBox.question(self, '确认', '确定添加书签？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:'''
    
    # 更通用的查找方式：查找包含 QMessageBox.question 和 add_bookmark 调用的块
    lines = content.split('\n')
    new_lines = []
    skip_until_add = False
    modified = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检查是否是触发书签添加的函数（如 toggle_bookmark 或快捷键处理）
        if 'QMessageBox.question' in line and not skip_until_add:
            # 向前找几行确认上下文
            context_start = max(0, i-5)
            context = ''.join(lines[context_start:i+1])
            if 'bookmark' in context.lower() or '书签' in context:
                # 找到确认对话框，开始跳过直到找到 add_bookmark 调用
                skip_until_add = True
                # 不添加当前行（question 行）
                i += 1
                continue
        
        if skip_until_add:
            if 'self.add_bookmark()' in line or 'add_bookmark(' in line:
                # 找到实际调用，添加缩进对齐的直接调用
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + 'self.add_bookmark()')
                skip_until_add = False
                modified = True
            # 跳过中间的 if reply == QMessageBox.Yes: 等行
            i += 1
            continue
            
        new_lines.append(line)
        i += 1
    
    if modified:
        content = '\n'.join(new_lines)
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 已移除确认弹窗（通用模式），现在添加书签无需确认！")
    else:
        print("⚠️ 未找到典型的确认弹窗代码，可能已经移除或使用不同实现")
# 验证修改
with open(main_file, 'r', encoding='utf-8') as f:
    final_content = f.read()
    if 'QMessageBox.question' in final_content and 'bookmark' in final_content.lower():
        print("⚠️ 警告：文件中仍存在书签相关的确认对话框代码")
    else:
        print("✅ 验证通过：确认弹窗已完全移除")