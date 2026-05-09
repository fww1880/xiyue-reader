import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找所有窗口标题设置
old_titles = [
    ('"本地小说阅读器"', '"喜阅"'),
    ("'本地小说阅读器'", "'喜阅'"),
]
count = 0
for old, new in old_titles:
    c = content.count(old)
    if c > 0:
        content = content.replace(old, new)
        count += c
        print(f"✅ 替换 {c} 处：{old} → {new}")
# 查找其他可能的标题引用
if 'setWindowTitle' in content:
    import re
    titles = re.findall(r'setWindowTitle\(["\']([^"\']+)["\']\)', content)
    for title in titles:
        if title != '喜阅' and '书签' not in title and '字体' not in title and '搜索' not in title and '关于' not in title:
            print(f"⚠️ 可能还有未修改的标题：{title}")
print(f"\n📝 共替换 {count} 处，已完成改名")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")