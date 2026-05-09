import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("🔍 查看第480-500行...")
for i in range(479, min(510, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
# 修复：self.refresh_bookmark_list() 应该在 try 块内
# 找到 open_file 方法里的 try 块
try_start = None
for i in range(479, 510):
    if 'try:' in lines[i]:
        try_start = i
        break
if try_start:
    # 检查 try 块结束位置
    for i in range(try_start, 510):
        if 'except Exception as e:' in lines[i]:
            except_line = i
            # 确保 self.refresh_bookmark_list() 在 except 之前
            if lines[487].strip() == 'self.refresh_bookmark_list()':
                # 检查缩进
                if lines[487].startswith('        '):
                    print("✅ 缩进正确")
                else:
                    lines[487] = '        ' + lines[487].lstrip()
                    print("✅ 已修复缩进")
                    with open(main_file, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
            break