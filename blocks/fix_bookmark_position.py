import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复1: 优化书签位置获取逻辑
# 原逻辑: cursor = self.text_edit.textCursor(); pos = cursor.position()
# 问题: 点击按钮时光标可能未更新，导致位置不变
# 新逻辑: 获取当前视口中心位置对应的字符索引
old_pos_logic = """        cursor = self.text_edit.textCursor()
        pos = cursor.position()"""
new_pos_logic = """        # 获取当前视口中心位置的字符索引，更符合阅读直觉
        center_point = self.text_edit.viewport().rect().center()
        cursor = self.text_edit.cursorForPosition(center_point)
        pos = cursor.position()"""
if old_pos_logic in content:
    content = content.replace(old_pos_logic, new_pos_logic)
    print("✅ 修复1：书签位置改为捕获屏幕中心位置")
else:
    print("⚠️ 未找到原位置获取代码，尝试查找变体...")
    # 备用方案：如果缩进不同，使用更宽松的替换
    if "cursor = self.text_edit.textCursor()" in content and "pos = cursor.position()" in content:
        # 逐行处理
        lines = content.split('\n')
        new_lines = []
        i = 0
        modified = False
        while i < len(lines):
            line = lines[i]
            if "cursor = self.text_edit.textCursor()" in line and "pos = cursor.position()" in lines[i+1] if i+1 < len(lines) else False:
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + '# 获取当前视口中心位置的字符索引')
                new_lines.append(' ' * indent + 'center_point = self.text_edit.viewport().rect().center()')
                new_lines.append(' ' * indent + 'cursor = self.text_edit.cursorForPosition(center_point)')
                new_lines.append(' ' * indent + 'pos = cursor.position()')
                i += 2
                modified = True
                continue
            new_lines.append(line)
            i += 1
        if modified:
            content = '\n'.join(new_lines)
            print("✅ 修复1：书签位置已优化（灵活匹配）")
        else:
            print("⚠️ 修复1：未能自动替换，请检查代码")
# 修复2: 确保跳转时位置准确（已修复过，再次确认）
# 检查跳转逻辑是否已经是 setPosition
if "cursor.setPosition(pos, QTextCursor.MoveAnchor)" in content:
    print("✅ 修复2：跳转逻辑已是精准模式 (setPosition)")
else:
    # 如果不是，强制替换
    old_jump = """        self.text_edit.moveCursor(QTextCursor.Start)
        for _ in range(pos):
            self.text_edit.moveCursor(QTextCursor.NextCharacter)
        self.text_edit.ensureCursorVisible()"""
    new_jump = """        # 使用 setPosition 直接跳转
        cursor = self.text_edit.textCursor()
        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()"""
    if old_jump in content:
        content = content.replace(old_jump, new_jump)
        print("✅ 修复2：跳转逻辑已更新为 setPosition")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 修复完成，正在验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")