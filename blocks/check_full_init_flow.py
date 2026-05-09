import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 提取完整的 init_ui 函数
print("🔍 提取完整的 init_ui 函数...")
init_ui_match = re.search(r'def init_ui\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if init_ui_match:
    init_ui_code = init_ui_match.group()
    print(f"init_ui 代码长度：{len(init_ui_code)}")
    # 查找 bm_list_widget 初始化的位置
    lines = init_ui_code.split('\n')
    for i, line in enumerate(lines):
        if 'bm_list_widget' in line or 'bookmark' in line.lower():
            print(f"\n第 {i} 行：{line.strip()}")
            # 显示上下文
            start = max(0, i-2)
            end = min(len(lines), i+3)
            print("  上下文:")
            for j in range(start, end):
                marker = ">>> " if j == i else "    "
                print(f"{marker}{j}: {lines[j]}")
# 检查是否有 create_bookmark_dock 或类似函数
print("\n\n🔍 查找创建书签侧边栏的完整函数...")
dock_funcs = re.findall(r'def (create_\w+|setup_\w+|init_\w+)\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
for func_name, func_code in [(m.group(1), m.group(0)) for m in re.finditer(r'def (create_\w+|setup_\w+|init_\w+)\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)]:
    if 'bookmark' in func_code.lower() or 'bm_' in func_code:
        print(f"\n📄 函数 {func_name}:")
        print(func_code[:800])
# 检查 add_bookmark 调用时 text_edit 是否存在
print("\n\n🔍 检查 text_edit 初始化...")
if 'self.text_edit =' in content:
    print("✅ text_edit 已初始化")
    # 找到初始化位置
    match = re.search(r'self\.text_edit\s*=\s*.*', content)
    if match:
        print(f"  初始化代码：{match.group()}")
else:
    print("❌ text_edit 未初始化！")
# 总结问题
print("\n\n🎯 可能的根本原因：")
print("1. bm_list_widget 初始化在 add_bookmark 被调用之前未完成")
print("2. text_edit 在某些情况下为 None")
print("3. 书签侧边栏根本没有正确创建")
print("4. 需要查看完整的 init_ui 流程")