import os
import ast
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 直接查找 keyboard_pagination 函数并完整修复它
pattern = r'def keyboard_pagination\(self, event\):.*?if key == Qt\.Key_Up:.*?# 向上翻页.*?\n(.*?)import sys'
match = re.search(pattern, content, re.DOTALL)
if match:
    print(f"⚠️ 找到问题：if 分支后没有缩进代码，直接到了 import sys")
    # 删除错误插入的 import sys，给 if 加上正确缩进
    content = content.replace('\n        if key == Qt.Key_Up:\n            # 向上翻页（滚动一行）\n\nimport sys', '\n        if key == Qt.Key_Up:\n            # 向上翻页（滚动一行）\n            if self.auto_scroll_enabled:\n                self.stop_auto_scroll()\n            # 向上滚动一行\n            vbar = self.text_edit.verticalScrollBar()\n            vbar.setValue(vbar.value() - vbar.singleStep())\n            event.accept()')
    print("✅ 已修复 keyboard_pagination 缩进问题")
# 重新整理整个文件，确保只有一个 resource_path 在开头
lines = content.split('\n')
new_lines = []
inserted_rp = False
for line in lines:
    stripped = line.strip()
    # 在第一个 class 之前插入 resource_path
    if not inserted_rp and stripped.startswith('class '):
        new_lines.append('')
        new_lines.append('# 定义资源路径处理函数（必须顶格，解决 sys._MEIPASS 问题）')
        new_lines.append('def resource_path(relative_path):')
        new_lines.append('    try:')
        new_lines.append('        base_path = sys._MEIPASS')
        new_lines.append('    except AttributeError:')
        new_lines.append('        base_path = os.path.dirname(os.path.abspath(__file__))')
        new_lines.append('    return os.path.join(base_path, relative_path)')
        new_lines.append('')
        inserted_rp = True
    # 跳过所有其他 resource_path 定义和重复注释
    if (stripped.startswith('def resource_path') or '# 定义资源路径' in stripped) and inserted_rp:
        continue
    new_lines.append(line)
# 保存
final_content = '\n'.join(new_lines)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(final_content)
# 语法检查
try:
    ast.parse(final_content)
    print("\n✅ Python 语法检查通过！")
except SyntaxError as e:
    print(f"\n❌ 仍有语法错误：{e} 第 {e.lineno} 行")
    lines_err = final_content.split('\n')
    start = max(0, e.lineno - 8)
    end = min(len(lines_err), e.lineno + 8)
    print("附近代码：")
    for i in range(start, end):
        marker = ">>>" if i == e.lineno - 1 else "   "
        print(f"{marker} {i+1:3d}: {repr(lines_err[i])}")
# 统计
print(f"\n📊 最终状态：")
print(f"   resource_path 定义：{final_content.count('def resource_path')}")
print(f"   import sys：{final_content.count('import sys')}")
print(f"   import os：{final_content.count('import os')}")