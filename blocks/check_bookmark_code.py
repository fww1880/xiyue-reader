import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找书签相关代码
print("=" * 60)
print("🔍 书签相关代码分析")
print("=" * 60)
# 1. 查找书签保存函数
bookmark_save = re.findall(r'def .*bookmark.*save.*|def .*save.*bookmark.*', content, re.IGNORECASE)
print(f"\n📌 书签保存函数：{bookmark_save}")
# 2. 查找书签加载函数
bookmark_load = re.findall(r'def .*bookmark.*load.*|def .*load.*bookmark.*', content, re.IGNORECASE)
print(f"📌 书签加载函数：{bookmark_load}")
# 3. 查找书签文件路径
bookmark_path = re.findall(r'bookmark.*\.(json|txt|dat|pkl)|\.bookmark', content, re.IGNORECASE)
print(f"📌 书签文件路径相关：{bookmark_path}")
# 4. 查找书签存储目录
bookmark_dir = re.findall(r'bookmark.*dir|bookmark.*folder|bookmark.*path', content, re.IGNORECASE)
print(f"📌 书签目录相关：{bookmark_dir}")
# 5. 查找 JSON 读写操作
json_read = re.findall(r'json\.(load|dump|dumps|loads)', content)
print(f"\n📌 JSON 读写操作：{json_read}")
# 6. 查找书签保存的触发点
save_triggers = re.findall(r'def .*close.*|def .*exit.*|def .*save.*', content, re.IGNORECASE)
print(f"📌 可能的保存触发函数：{save_triggers}")
# 7. 输出书签相关代码片段
print("\n" + "=" * 60)
print("📄 书签相关代码片段")
print("=" * 60)
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'bookmark' in line.lower() or '书签' in line:
        print(f"  L{i:>4}: {line.strip()}")