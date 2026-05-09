import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 搜索所有包含 bookmark 的函数定义
print("🔍 搜索所有书签相关函数...")
patterns = [
    r'def \w*bookmark\w*\(self\):',
    r'def add_bm\(self\):',
    r'def save_bm\(self\):',
    r'def refresh_bm\(self\):'
]
for pattern in patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"\n✅ 找到匹配 '{pattern}':")
        for m in matches:
            print(f"  {m}")
# 搜索所有包含"书签"中文的函数
print("\n🔍 搜索包含'书签'的代码...")
lines_with_bookmark = []
for i, line in enumerate(content.split('\n')):
    if '书签' in line or 'add_bookmark' in line or 'bm_' in line:
        lines_with_bookmark.append((i+1, line.strip()))
print(f"找到 {len(lines_with_bookmark)} 行相关代码:")
for line_no, line in lines_with_bookmark[:30]:  # 显示前30行
    print(f"{line_no:4d}: {line}")
# 检查工具栏和菜单中连接的函数名
print("\n🔍 检查工具栏/菜单连接的函数名...")
connect_matches = re.findall(r'connect\(self\.(\w+)\)', content)
bookmark_related = [m for m in connect_matches if 'bookmark' in m.lower() or 'bm' in m.lower()]
print(f"找到的连接：{bookmark_related}")
# 查找实际定义的函数
print("\n🔍 查找类中所有方法定义...")
method_pattern = r'def (\w+)\(self\):'
all_methods = re.findall(method_pattern, content)
bookmark_methods = [m for m in all_methods if 'bookmark' in m.lower() or 'bm' in m.lower()]
print(f"类中的书签相关方法：{bookmark_methods}")