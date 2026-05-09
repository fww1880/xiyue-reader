import os, subprocess, time, psutil, sys
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
# 先检查代码中可能的错误
print("🔍 深度检查代码...")
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 提取 refresh_bookmark_list 函数
import re
match_refresh = re.search(r'def refresh_bookmark_list\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_refresh:
    refresh_code = match_refresh.group()
    print(f"📄 refresh_bookmark_list 完整代码：\n{refresh_code}")
    # 检查可能的问题
    if 'self.bookmark_widget' in refresh_code and 'hasattr' not in refresh_code:
        print("\n⚠️ 警告：refresh_bookmark_list 直接访问 self.bookmark_widget，没有检查是否存在！")
    if 'self.bookmark_list' in refresh_code and 'hasattr' not in refresh_code:
        print("⚠️ 警告：refresh_bookmark_list 直接访问 self.bookmark_list，没有检查是否存在！")
    if '.clear()' in refresh_code:
        print("✅ 有 .clear() 操作")
    if 'for bookmark in' in refresh_code:
        print("✅ 有遍历书签列表")
# 提取 get_position_preview 函数
match_preview = re.search(r'def get_position_preview\(self, pos\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_preview:
    preview_code = match_preview.group()
    print(f"\n📄 get_position_preview 完整代码：\n{preview_code}")
    # 检查可能的问题
    if 'self.text_edit' in preview_code and 'hasattr' not in preview_code:
        print("\n⚠️ 警告：get_position_preview 直接访问 self.text_edit，没有检查是否存在！")
    if '.document()' in preview_code:
        print("✅ 访问了 document")
# 提取 add_bookmark 函数
match_add = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_add:
    add_code = match_add.group()
    print(f"\n📄 add_bookmark 完整代码：\n{add_code}")
    # 检查调用顺序
    lines = add_code.split('\n')
    for i, line in enumerate(lines):
        if 'self.get_position_preview' in line:
            print(f"\n✅ 第 {i} 行调用 get_position_preview")
        if 'self.save_bookmarks' in line:
            print(f"✅ 第 {i} 行调用 save_bookmarks")
        if 'self.refresh_bookmark_list' in line:
            print(f"✅ 第 {i} 行调用 refresh_bookmark_list")
# 检查 bookmark_widget 是否初始化
print("\n🔍 检查 bookmark_widget 初始化...")
if 'self.bookmark_widget =' in content:
    print("✅ bookmark_widget 已初始化")
else:
    print("❌ bookmark_widget 未初始化！这是闪退原因！")
# 检查 bookmark_list 是否初始化
print("\n🔍 检查 bookmark_list 初始化...")
if 'self.bookmark_list =' in content or 'self.bookmark_list = []' in content:
    print("✅ bookmark_list 已初始化")
else:
    print("❌ bookmark_list 未初始化！这也是闪退原因！")
# 总结可能的问题
print("\n🎯 可能的闪退原因：")
print("1. refresh_bookmark_list 访问了不存在的 widget")
print("2. get_position_preview 访问了不存在的 text_edit")
print("3. bookmark_widget 或 bookmark_list 未初始化")
print("4. 其他属性访问错误")