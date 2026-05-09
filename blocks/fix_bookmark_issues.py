import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修改1: 移除成功提示弹窗 (L926)
old1 = "        QMessageBox.information(self, \"成功\", f\"书签已添加！\\n时间：{timestamp}\")"
new1 = "        self.status_bar.showMessage(f\"✅ 书签已添加：{timestamp}\", 3000)"
if old1 in content:
    content = content.replace(old1, new1)
    print("✅ 修复1：成功提示弹窗改为状态栏显示")
else:
    print("⚠️ 修复1：未找到成功弹窗代码")
# 修改2: 修复书签跳转逻辑（用 setPosition 替代 for 循环逐字符移动）
old2 = """        self.text_edit.moveCursor(QTextCursor.Start)
        for _ in range(pos):
            self.text_edit.moveCursor(QTextCursor.NextCharacter)
        self.text_edit.ensureCursorVisible()"""
new2 = """        # 使用 setPosition 直接跳转（更准确更高效）
        cursor = self.text_edit.textCursor()
        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()"""
if old2 in content:
    content = content.replace(old2, new2)
    print("✅ 修复2：书签跳转逻辑改为 setPosition 直接跳转")
else:
    print("⚠️ 修复2：未找到旧的跳转代码，尝试查找变体...")
    # 可能缩进不同，尝试更灵活的匹配
    lines = content.split('\n')
    new_lines = []
    i = 0
    modified = False
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # 检查是否是旧的跳转代码块开头
        if stripped == 'self.text_edit.moveCursor(QTextCursor.Start)':
            # 检查后续几行
            if i+2 < len(lines):
                next1 = lines[i+1].strip()
                next2 = lines[i+2].strip()
                if next1.startswith('for _ in range(pos):') and next2 == 'self.text_edit.moveCursor(QTextCursor.NextCharacter)':
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + '# 使用 setPosition 直接跳转（更准确更高效）')
                    new_lines.append(' ' * indent + 'cursor = self.text_edit.textCursor()')
                    new_lines.append(' ' * indent + 'cursor.setPosition(pos, QTextCursor.MoveAnchor)')
                    new_lines.append(' ' * indent + 'self.text_edit.setTextCursor(cursor)')
                    new_lines.append(' ' * indent + 'self.text_edit.ensureCursorVisible()')
                    i += 4  # 跳过原代码的4行
                    modified = True
                    continue
        new_lines.append(line)
        i += 1
    if modified:
        content = '\n'.join(new_lines)
        print("✅ 修复2：书签跳转逻辑已修复（灵活匹配模式）")
    else:
        print("⚠️ 修复2：仍未找到旧的跳转代码")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 修改完成，正在验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")