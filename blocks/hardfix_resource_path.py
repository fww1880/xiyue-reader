import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 把 resource_path 直接插入到文件最开头，所有 import 之后
# 首先找到文件开头所有 import 结束的位置
lines = content.split('\n')
first_class_idx = 0
for i, line in enumerate(lines):
    if line.strip().startswith('class '):
        first_class_idx = i
        break
print(f"📌 第一个 class 在第 {first_class_idx} 行")
# 插入 resource_path 到 import 之后，class 之前
fixed_rp = '''
# 定义资源路径处理函数，必须放在文件开头避免 sys 访问错误
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
'''
# 删除原来的 resource_path 定义
content = re.sub(r'def resource_path\(.*?\).*?(?=\n\n|\ndef |\nclass |\Z)', '', content, flags=re.DOTALL)
# 在第一个 class 之前插入我们干净的 resource_path
lines = content.split('\n')
new_lines = lines[:first_class_idx] + [fixed_rp] + lines[first_class_idx:]
new_content = '\n'.join(new_lines)
print("✅ 已将 resource_path 移到文件开头（import 之后，class 之前）")
# 确保调用没问题（移除所有其他定义）
if new_content.count('def resource_path') > 1:
    print(f"⚠️  还有 {new_content.count('def resource_path') - 1} 个多余定义，将删除...")
    # 删除后面的定义
    matches = list(re.finditer(r'def resource_path\(.*?\).*?(?=\n\n|\ndef |\nclass |\Z)', new_content, flags=re.DOTALL))
    if len(matches) > 1:
        # 删除后面的所有重复定义
        for m in matches[1:]:
            new_content = new_content.replace(m.group(), '')
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("💾 文件已保存")
# 验证
with open(main_file, 'r', encoding='utf-8') as f:
    final_content = f.read()
print(f"\n📋 验证：")
print(f"   resource_path 定义数量：{final_content.count('def resource_path')}")
idx = final_content.find('def resource_path')
if idx >= 0:
    end = idx + 300
    print(final_content[idx:end])