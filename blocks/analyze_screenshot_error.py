import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("🔍 检查 refresh_bookmark_list 方法...")
start = content.find('def refresh_bookmark_list')
if start != -1:
    end = content.find('\n    def ', start + 1)
    if end == -1:
        end = len(content)
    method = content[start:end]
    print(method)
else:
    print("❌ 找不到 refresh_bookmark_list 方法！")
print("\n\n🔍 检查 bookmark_list 初始化...")
if 'self.bookmark_list = []' in content:
    print("✅ 已找到初始化代码")
else:
    print("❌ 未找到初始化代码，可能导致 NoneType 错误！")