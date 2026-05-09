import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 用行读取方式更可靠
lines = content.split('\n')
# 第一步：找到 create_tool_bar 并在末尾添加保存 toolbar
in_create_toolbar = False
added_save = False
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'def create_tool_bar(self):' in line:
        in_create_toolbar = True
    if in_create_toolbar and 'toolbar.addAction(focus_action)' in line:
        # 下一行添加保存
        new_lines.append('        self.toolbar = toolbar')
        new_lines.append('        self.base_icon_size = 22')
        added_save = True
        print("✅ 在 create_tool_bar 末尾添加了 self.toolbar = toolbar")
print(f"添加保存结果：{added_save}")
# 第二步：添加 resizeEvent 方法，放到文件末尾前
has_resize_event = any('def resizeEvent' in line for line in lines)
if not has_resize_event:
    # 找到最后一个方法的位置，插入到它后面
    last_def_pos = 0
    for i, line in enumerate(new_lines):
        if line.strip().startswith('def '):
            last_def_pos = i
    # 在它后面插入
    insert_lines = [
        '',
        '    def resizeEvent(self, event):',
        '        \"\"\"窗口大小变化时自适应工具栏图标大小\"\"\"',
        '        super().resizeEvent(event)',
        '        # 自适应工具栏图标大小，根据窗口宽度动态调整',
        '        if hasattr(self, \"toolbar\"):',
        '            width = self.width()',
        '            # 根据窗口宽度比例计算合适的图标大小',
        '            # 窗口越大，图标越大；窗口越小，图标越小',
        '            new_size = max(16, min(32, int(width / 60)))',
        '            self.toolbar.setIconSize(QSize(new_size, new_size))',
    ]
    # 插入到最后一个 def 之后
    insertion_point = last_def_pos + 1
    for line in insert_lines:
        new_lines.insert(insertion_point, line)
        insertion_point += 1
    print("✅ 添加了 resizeEvent 自适应方法")
else:
    # 已有 resizeEvent，插入我们的代码
    print("⚠️ resizeEvent 已存在，跳过添加")
# 第三步：修改 CSS，减小固定宽度
content_new = '\n'.join(new_lines)
# 修改 min-width: 60px -> min-width: 40px
# 修改 padding: 8px 14px -> padding: 4px 2px
content_new = content_new.replace('min-width: 60px', 'min-width: 40px')
content_new = content_new.replace('padding: 8px 14px', 'padding: 4px 2px')
print("✅ 修改了 CSS 固定宽度和内边距")
# 保存文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content_new)
print("💾 已保存修改")
# 语法检查
import ast
try:
    ast.parse(content_new)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")