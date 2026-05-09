import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修改 CSS：去掉固定 min-width，改为百分比和弹性布局
old_macaron_css = r'            QToolButton {\n                border: none;\n                border-radius: 6px;\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 #ffffff, stop:1 #E3F2FD);\n                padding: 4px 8px;\n                margin: 2px;\n                min-width: 60px;\n                color: #1565C0;\n                font-weight: bold;\n            }'
new_macaron_css = r'            QToolButton {\n                border: none;\n                border-radius: 6px;\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 #ffffff, stop:1 #E3F2FD);\n                padding: 4px 1px;\n                margin: 2px;\n                min-width: 40px;\n                color: #1565C0;\n                font-weight: bold;\n            }'
# 同时修改下面第二个 QToolButton 块的固定 padding 和字体大小
old_qtoolbutton_second = r'             QToolButton {\n                background-color: #FFFFFF;\n                border: 2px solid #AEC6CF; /* 马卡龙蓝边框 */\n                border-radius: 12px;\n                padding: 8px 14px;\n                color: #555555;\n                font-size: 14px; /* 字体加大 */\n                font-weight: bold;\n                font-family: "Microsoft YaHei";\n            }'
new_qtoolbutton_second = r'             QToolButton {\n                background-color: #FFFFFF;\n                border: 2px solid #AEC6CF; /* 马卡龙蓝边框 */\n                border-radius: 12px;\n                padding: 4px 2px;\n                color: #555555;\n                font-weight: bold;\n                font-family: "Microsoft YaHei";\n            }'
if old_macaron_css in content:
    content = content.replace(old_macaron_css, new_macaron_css)
    print("✅ 已修改第一个 QToolButton CSS（减小固定宽度）")
else:
    print("⚠️ 未找到第一个 QToolButton CSS 块")
if old_qtoolbutton_second in content:
    content = content.replace(old_qtoolbutton_second, new_qtoolbutton_second)
    print("✅ 已修改第二个 QToolButton CSS（减小固定内边距）")
else:
    print("⚠️ 未找到第二个 QToolButton CSS 块")
# 2. 在 __init__ 末尾保存 toolbar 实例为 self.toolbar
# 查找 create_tool_bar 末尾
# 找到 create_tool_bar 的位置，确保 toolbar 保存为成员变量
# 原有代码末尾是：
#   653:         toolbar.addAction(focus_action)
#   654: 
#   655:     def open_file_dialog(self):
# 需要把 toolbar 保存为 self.toolbar = toolbar
# 找到工具栏创建部分：
#     def create_tool_bar(self):
#        ... 
#        toolbar.addAction(focus_action)
#
# 在最后添加：
#        self.toolbar = toolbar
#        self.base_icon_size = 22
#        self.base_font_size = 14
content = re.sub(
    r'(        focus_action\.triggered_connect.*focus_action\).*\n        toolbar\.addAction\(focus_action\)\n)',
    r'\1        self.toolbar = toolbar\n        self.base_icon_size = 22\n        self.base_font_size = 14\n',
    flags=re.DOTALL
)
print("✅ 已添加工具栏成员变量保存")
# 3. 添加 resizeEvent 事件处理，窗口大小变化时自动调整图标大小
# 查找是否已有 resizeEvent
if 'def resizeEvent' in content:
    print("⚠️ 已存在 resizeEvent，需要合并")
    # 找到现有 resizeEvent 并添加我们的代码
    content = re.sub(
        r'(def resizeEvent\(self, event\):.*?)(?=\n    def |\nclass |\Z)',
        r'\1        # 自适应工具栏图标大小\n        if hasattr(self, \"toolbar\"):\n            width = self.width()\n            # 根据窗口宽度计算图标大小\n            new_size = max(16, min(32, int(width / 60)))\n            self.toolbar.setIconSize(QSize(new_size, new_size))\n',
        flags=re.DOTALL
    )
else:
    print("➕ 添加新的 resizeEvent 方法")
    # 在最后添加 resizeEvent 方法，放在 __init__ 之后？我们找到最后一个方法然后添加
    # 或者在类末尾添加
    # 先找到类结束位置，直接加在末尾
    # 找到 NovelReaderMainWindow 类的末尾
    insert_code = '''
    def resizeEvent(self, event):
        \"\"\"窗口大小变化时自适应工具栏图标大小\"\"\"
        super().resizeEvent(event)
        # 自适应工具栏图标大小，根据窗口宽度动态调整
        if hasattr(self, \"toolbar\"):
            width = self.width()
            # 根据窗口宽度比例计算合适的图标大小
            # 窗口越大，图标越大；窗口越小，图标越小
            new_size = max(16, min(32, int(width / 60)))
            self.toolbar.setIconSize(QSize(new_size, new_size))
'''
    # 在类的末尾插入（找到最后一个方法然后加在它后面）
    # 这里简化处理，在最后一个 def 之后找一个位置插入
    # 查找所有 def ，找到最后一个
    matches = list(re.finditer(r'    def \w+', content))
    if matches:
        last_match = matches[-1]
        # 找到这个方法的结束位置
        pos = content.find('\n    def ', last_match.start())
        if pos == -1:
            pos = len(content)
        content = content[:pos] + insert_code + '\n' + content[pos:]
        print("✅ 已添加 resizeEvent 自适应处理")
# 保存文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存修改")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")