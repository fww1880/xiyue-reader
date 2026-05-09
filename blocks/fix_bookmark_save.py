import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查 save_bookmarks 方法
if 'def save_bookmarks(self):' in content:
    print("✅ 找到 save_bookmarks 方法")
    # 查找并加强它
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def save_bookmarks(self):' in line:
            print(f"  L{i+1}: {line.strip()}")
            # 打印接下来的几行看看实现
            for j in range(i+1, min(i+10, len(lines))):
                print(f"  L{j+1}: {lines[j].strip()}")
            break
else:
    print("❌ 未找到 save_bookmarks 方法")
# 检查 load_bookmarks 方法
print("\n检查 load_bookmarks 方法：")
if 'def load_bookmarks(self):' in content:
    print("✅ 找到 load_bookmarks 方法")
else:
    print("❌ 未找到 load_bookmarks 方法")