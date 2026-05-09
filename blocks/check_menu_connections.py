import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找创建菜单栏的函数
print("🔍 查找 create_menu_bar 函数...")
menu_match = re.search(r'def create_menu_bar\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if menu_match:
    menu_code = menu_match.group()
    print(f"create_menu_bar 代码长度：{len(menu_code)}")
    # 查找书签相关的菜单项
    lines = menu_code.split('\n')
    for i, line in enumerate(lines):
        if '书签' in line or 'add_bookmark' in line:
            print(f"\n第 {i} 行：{line.strip()}")
            # 显示上下文
            start = max(0, i-2)
            end = min(len(lines), i+5)
            print("  上下文:")
            for j in range(start, end):
                marker = ">>> " if j == i else "    "
                print(f"{marker}{j}: {lines[j]}")
# 查找工具栏创建函数
print("\n\n🔍 查找 create_tool_bar 中的书签按钮...")
toolbar_match = re.search(r'def create_tool_bar\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if toolbar_match:
    toolbar_code = toolbar_match.group()
    lines = toolbar_code.split('\n')
    for i, line in enumerate(lines):
        if '书签' in line or 'add_bookmark' in line:
            print(f"\n第 {i} 行：{line.strip()}")
            start = max(0, i-2)
            end = min(len(lines), i+5)
            print("  上下文:")
            for j in range(start, end):
                marker = ">>> " if j == i else "    "
                print(f"{marker}{j}: {lines[j]}")
# 查找右键菜单相关函数
print("\n\n🔍 查找右键菜单相关函数...")
context_funcs = ['show_bookmark_context_menu', 'contextMenuEvent', 'createContextMenu']
for func_name in context_funcs:
    pattern = rf'def {func_name}\(self\):.*?(?=\n    def |\nclass |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(f"\n📄 函数 {func_name}:")
        func_code = match.group()
        print(func_code[:600])
# 检查 add_bookmark 函数的完整代码
print("\n\n🔍 再次检查 add_bookmark 的完整代码（逐行分析）...")
add_match = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if add_match:
    add_code = add_match.group()
    lines = add_code.split('\n')
    print("逐行分析:")
    for i, line in enumerate(lines):
        print(f"{i:3d}: {line}")
        # 标记可能的错误点
        if 'self.text_edit.viewport()' in line:
            print(f"      ⚠️ 访问 text_edit.viewport()")
        if 'self.text_edit.cursorForPosition' in line:
            print(f"      ⚠️ 调用 cursorForPosition")
        if 'self.get_position_preview' in line:
            print(f"      ⚠️ 调用 get_position_preview")
# 总结
print("\n\n🎯 下一步行动：")
print("1. 检查 add_bookmark 中是否有未初始化的属性访问")
print("2. 检查右键菜单是否正确连接")
print("3. 可能需要添加 try-except 来捕获具体错误")