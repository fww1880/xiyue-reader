import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 精确输出 resource_path 函数定义
print("=" * 60)
print("📄 resource_path 函数完整内容")
print("=" * 60)
idx = content.find('def resource_path')
if idx >= 0:
    # 找到函数结束位置（下一个 def 或 class）
    end_idx = content.find('\n\n', idx)
    if end_idx == -1:
        end_idx = content.find('\ndef ', idx)
    if end_idx == -1:
        end_idx = content.find('\nclass ', idx)
    if end_idx == -1:
        end_idx = idx + 500
    print(content[idx:end_idx])
else:
    print("❌ 未找到 resource_path 函数定义！")
# 检查 import sys 和 import os 的位置
print("\n" + "=" * 60)
print("🔍 检查 import 语句")
print("=" * 60)
for line in content.split('\n')[:30]:
    if 'import' in line:
        print(f"  {line.strip()}")
# 检查是否有多个 resource_path 定义
count = content.count('def resource_path')
print(f"\n📌 resource_path 定义数量：{count}")
# 检查是否有多个 setWindowIcon
count2 = content.count('setWindowIcon')
print(f"📌 setWindowIcon 调用数量：{count2}")
# 检查是否有多个 icon_path
count3 = content.count('icon_path')
print(f"📌 icon_path 出现次数：{count3}")