import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("🔍 检查工具栏书签按钮绑定...")
# 找到工具栏创建代码
if 'add_bookmark' in content:
    # 查找书签按钮连接
    if 'connect' in content and 'show_bookmark_list' in content:
        print("✅ 找到 show_bookmark_list 绑定")
    else:
        print("❌ 可能绑定错误")
# 检查添加到工具栏的代码
lines = content.split('\n')
for i, line in enumerate(lines):
    if '书签' in line and 'QAction' in line:
        print(f"L{i+1}: {line.strip()}")
        if i+2 < len(lines):
            print(f"  -> 连接: {lines[i+2].strip()}")
# 修复：工具栏"书签"按钮应该打开/刷新显示，而不是弹窗
# 查找书签按钮连接
old_connect = None
for i, line in enumerate(lines):
    if '.triggered.connect' in line and 'show_bookmark_list' in line:
        print(f"✅ 已找到连接行 L{i+1}: {line.strip()}")
        break
# 检查添加书签后是否刷新
if 'self.refresh_bookmark_list()' not in content.split('def add_bookmark')[1]:
    print("⚠️ 添加书签方法中没有刷新列表")
    # 添加刷新
    old_add_end = '''        QMessageBox.information(self, "成功", f"书签已添加！\\n时间：{timestamp}")'''
    new_add_end = '''        QMessageBox.information(self, "成功", f"书签已添加！\\n时间：{timestamp}")
        self.refresh_bookmark_list()'''
    content = content.replace(old_add_end, new_add_end)
    print("✅ 添加了添加书签后刷新列表")
else:
    print("✅ 添加书签后已有刷新")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n🚀 修复完成！")