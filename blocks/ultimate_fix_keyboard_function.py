import os
import ast
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 第一步：彻底切除所有错误插入的 resource_path，只保留一个在最开头
lines = content.split('\n')
cleaned_lines = []
found_correct_rp = False
inside_bad_rp = False
for line in lines:
    stripped = line.strip()
    # 如果还没找到正确的 resource_path，并且遇到一个顶格的，保留它
    if not found_correct_rp and stripped.startswith('def resource_path(') and (len(line) - len(line.lstrip()) == 0):
        cleaned_lines.append(line)
        found_correct_rp = True
        inside_bad_rp = False
        continue
    # 如果已经找到了正确的，跳过所有其他 resource_path 定义
    if found_correct_rp and (stripped.startswith('def resource_path(') or '# 定义资源路径' in stripped):
        inside_bad_rp = True
        continue
    # 如果在错误的 resource_path 中，继续跳过直到缩进恢复
    if inside_bad_rp:
        # 当遇到缩进比 resource_path 定义小，说明错误区域结束了
        if stripped and len(line) - len(line.lstrip()) <= 0:
            inside_bad_rp = False
        else:
            continue
    cleaned_lines.append(line)
# 第二步：确保 keyboard_pagination 函数是完整的
# 重新构建完整的 keyboard_pagination 函数
full_kb_func = '''    def keyboard_pagination(self, event):
        """键盘翻页：方向键、PageUp/PageDown、空格键"""
        key = event.key()
        if key == Qt.Key_Up:
            # 向上翻页（滚动一行）
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            # 向上滚动一行
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.singleStep())
            event.accept()
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() - 10
            )
        elif key == Qt.Key_Down:
            # 向下翻页（滚动一行）
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().value() + 10
            )
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            event.accept()
        elif key == Qt.Key_PageUp:
            # 向上翻一页
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.pageStep())
            event.accept()
        elif key == Qt.Key_PageDown:
            # 向下翻一页
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            vbar = self.text_edit.verticalScrollBar()
            vbar.setValue(vbar.value() + vbar.pageStep())
            event.accept()
        elif key == Qt.Key_Space:
            # 空格触发自动滚屏开关
            if self.auto_scroll_enabled:
                self.stop_auto_scroll()
            else:
                self.start_auto_scroll()
            event.accept()
'''
# 第三步：合并文件
# 找到 keyboard_pagination 开始位置，替换掉整个函数
content_cleaned = '\n'.join(cleaned_lines)
pattern = r'def keyboard_pagination\(self, event\):.*?(?=\n    def |\n    class |\Z)'
match = re.search(pattern, content_cleaned, re.DOTALL)
if match:
    print(f"✅ 找到 keyboard_pagination 函数，长度 {len(match.group())}，替换为完整版本")
    content_final = content_cleaned.replace(match.group(), full_kb_func.strip('\n'))
else:
    print("⚠️ 未找到 keyboard_pagination 函数，使用已清理版本")
    content_final = content_cleaned
# 第四步：重新确保 resource_path 只存在一个，在最开头，第一个 class 之前
lines_final = content_final.split('\n')
lines_ultimate = []
inserted_final = False
for line in lines_final:
    stripped = line.strip()
    if not inserted_final and stripped.startswith('class '):
        # 如果还没插入，在第一个 class 之前插入 resource_path
        # 检查是否已经插入
        has_rp = any('def resource_path' in l for l in lines_ultimate)
        if not has_rp:
            lines_ultimate.append('')
            lines_ultimate.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
            lines_ultimate.append('def resource_path(relative_path):')
            lines_ultimate.append('    try:')
            lines_ultimate.append('        base_path = sys._MEIPASS')
            lines_ultimate.append('    except AttributeError:')
            lines_ultimate.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
            lines_ultimate.append('    return os.path.join(base_path, relative_path)')
            lines_ultimate.append('')
        inserted_final = True
    lines_ultimate.append(line)
# 第五步：保存并语法检查
content_ultimate = '\n'.join(lines_ultimate)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content_ultimate)
try:
    ast.parse(content_ultimate)
    print("\n✅ 终极修复完成！Python 语法检查通过！")
except SyntaxError as e:
    print(f"\n❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    lines_err = content_ultimate.split('\n')
    start = max(0, e.lineno - 15)
    end = min(len(lines_err), e.lineno + 15)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
print(f"\n📊 最终统计：")
print(f"   resource_path 定义：{content_ultimate.count('def resource_path')}")
print(f"   import sys：{content_ultimate.count('import sys')}")
print(f"   import os：{content_ultimate.count('import os')}")