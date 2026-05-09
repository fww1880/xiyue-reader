import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 show_bookmark_list 方法并修复 - 它缺少方法体
# 同时修复 show_about_dialog 的缩进
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # 修复 show_bookmark_list 方法 - 添加 pass 方法体
    if 'def show_bookmark_list(self):' in line:
        new_lines.append(line)
        # 检查下一行是否直接是下一个 def
        if i+1 < len(lines) and '    def ' in lines[i+1]:
            # 添加方法体
            new_lines.append('        """显示书签列表（显示书架面板并刷新）"""\n')
            new_lines.append('        self.bookshelf_dock.show()\n')
            new_lines.append('        self.refresh_bookmark_list()\n')
            i += 1
            continue
        else:
            # 已经有方法体了，跳过
            i += 1
            continue
    # 修复 show_about_dialog - 替换为正确缩进
    if 'def show_about_dialog(self):' in line:
        new_lines.append('    def show_about_dialog(self):\n')
        new_lines.append('        """显示关于对话框"""\n')
        new_lines.append('        from PyQt5.QtWidgets import QMessageBox\n')
        new_lines.append('        QMessageBox.about(self, "关于 喜阅",\n')
        new_lines.append('            "<h2>📖 木木的喜阅</h2>"\n')
        new_lines.append('            "<p>版本：2026.5</p>"\n')
        new_lines.append('            "<hr>"\n')
        new_lines.append('            "<p>一款本地小说阅读器，让阅读更愉悦。</p>"\n')
        new_lines.append('            "<p>支持多种格式、书签管理、自动滚屏、翻页动画。</p>"\n')
        new_lines.append('            "<hr>"\n')
        new_lines.append('            "<p style=\'color: #888;\'>© 2026 木木</p>"\n')
        new_lines.append('        )\n')
        # 跳过原方法的所有行
        i += 1
        while i < len(lines) and (lines[i].startswith('        ') or lines[i].strip() == '' or lines[i].startswith('            ')):
            i += 1
        continue
    new_lines.append(line)
    i += 1
content = ''.join(new_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 已修复 show_bookmark_list 和 show_about_dialog 方法")
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")