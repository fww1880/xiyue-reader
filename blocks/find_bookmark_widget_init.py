import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找初始化书签相关的代码
print("🔍 查找书签侧边栏初始化代码...")
# 搜索 bm_list_widget 或 bookmark_widget 的初始化
patterns = [
    r'self\.bm_list_widget\s*=\s*.*',
    r'self\.bookmark_widget\s*=\s*.*',
    r'self\.bookmark_dock\s*=\s*.*',
    r'QDockWidget.*书签',
    r'QListWidget.*书签'
]
for pattern in patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"\n✅ 找到匹配 '{pattern}':")
        for m in matches[:5]:  # 最多显示5个
            print(f"  {m}")
# 查找 init_ui 或 create_menu 中关于书签的部分
print("\n🔍 查找菜单和工具栏中的书签相关代码...")
menu_matches = re.findall(r'addAction.*书签|QAction.*书签|connect.*add_bookmark', content)
if menu_matches:
    print("✅ 找到书签菜单/工具栏连接:")
    for m in menu_matches:
        print(f"  {m}")
# 查找完整的 __init__ 方法
print("\n🔍 查找 __init__ 方法中的初始化...")
init_match = re.search(r'def __init__\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if init_match:
    init_code = init_match.group()
    # 提取前100行
    lines = init_code.split('\n')[:100]
    for i, line in enumerate(lines):
        if 'bookmark' in line.lower() or 'bm_' in line:
            print(f"  第 {i} 行：{line.strip()}")
# 查找 create_bookmark_dock 或类似函数
print("\n🔍 查找创建书签侧边栏的函数...")
dock_func = re.search(r'def (create_\w*|init_\w*)\(self\):.*?bookmark|def (create_\w*|init_\w*)\(self\):.*?bm_', content, re.DOTALL | re.IGNORECASE)
if dock_func:
    print(f"✅ 找到相关函数:\n{dock_func.group()[:500]}")
else:
    print("❌ 没找到专门的书签侧边栏初始化函数")
# 总结
print("\n🎯 分析结论:")
print("1. refresh_bookmark_list 使用 self.bm_list_widget")
print("2. 但可能 bm_list_widget 从未被初始化")
print("3. 需要找到哪里应该初始化 bm_list_widget")