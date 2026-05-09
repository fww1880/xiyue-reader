import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
print("=" * 70)
print("📋 完整书签相关代码审计")
print("=" * 70)
# 1. 检查所有书签相关方法
methods = ['add_bookmark', 'show_bookmark_list', 'refresh_bookmark_list', 
           'jump_to_selected_bookmark', 'delete_selected_bookmark',
           'save_bookmarks', 'load_bookmarks', 'get_current_time']
for method in methods:
    start = content.find(f'def {method}')
    if start == -1:
        print(f"❌ 方法 {method} 不存在！")
    else:
        end = content.find('\n    def ', start + 1)
        if end == -1:
            end = content.find('\nclass ', start + 1)
        if end == -1:
            end = len(content)
        method_code = content[start:end]
        print(f"\n✅ 方法 {method} 存在（{end-start}字符）")
        # 检查方法体缩进
        first_line_end = method_code.find('\n')
        body = method_code[first_line_end+1:]
        if body.strip():
            first_body_line = body.split('\n')[0]
            leading = len(first_body_line) - len(first_body_line.lstrip())
            if leading != 8:
                print(f"  ⚠️ 方法体缩进异常：leading={leading}，应为8")
# 2. 检查工具栏按钮
print("\n" + "=" * 70)
print("🔍 工具栏书签按钮")
print("=" * 70)
for i, line in enumerate(lines):
    if '书签' in line and ('QAction' in line or 'triggered' in line):
        print(f"L{i+1}: {line.strip()}")
# 3. 检查书架面板中的书签控件
print("\n" + "=" * 70)
print("🔍 书架面板书签控件")
print("=" * 70)
for i, line in enumerate(lines):
    if 'bm_label' in line or 'bm_list_widget' in line:
        print(f"L{i+1}: {line.strip()}")
# 4. 检查 add_bookmark 方法完整代码
print("\n" + "=" * 70)
print("🔍 add_bookmark 完整方法")
print("=" * 70)
start = content.find('def add_bookmark')
if start != -1:
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    print(content[start:end])
# 5. 检查 show_bookmark_list 完整代码
print("\n" + "=" * 70)
print("🔍 show_bookmark_list 完整方法")
print("=" * 70)
start = content.find('def show_bookmark_list')
if start != -1:
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    print(content[start:end])