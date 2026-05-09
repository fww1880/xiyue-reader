import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 清理重复的 import sys / import os（只保留文件顶部原有的）
lines = content.split('\n')
cleaned_lines = []
seen_imports = set()
for line in lines:
    stripped = line.strip()
    # 跳过重复的 import sys / import os（但保留第一个）
    if stripped in ('import sys', 'import os'):
        if stripped in seen_imports:
            continue
        seen_imports.add(stripped)
    cleaned_lines.append(line)
content = '\n'.join(cleaned_lines)
print("✅ 已清理重复的 import sys / import os")
# 2. 彻底替换 resource_path 函数
old_rp = '''def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    try:
        # PyInstaller 打包后会设置 _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境下使用脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)'''
new_rp = '''def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)'''
if old_rp in content:
    content = content.replace(old_rp, new_rp)
    print("✅ 已修复 resource_path 函数（移除多余 return）")
else:
    # 模糊替换：找到 def resource_path 到下一个 def 之间的内容，替换掉
    rp_match = re.search(r'def resource_path\(.*?\):.*?(?=\n\ndef |\nclass |\Z)', content, re.DOTALL)
    if rp_match:
        content = content.replace(rp_match.group(), new_rp)
        print("✅ 已全局替换 resource_path 函数")
# 3. 确保 setWindowIcon 使用正确的调用方式（移除 icon_path 变量，直接调用）
content = re.sub(
    r'self\.setWindowIcon\(QIcon\(resource_path\([^)]+\)\)\)',
    "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))",
    content
)
print("✅ 已确保 setWindowIcon 调用正确")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 最终修复已保存")
# 验证
print("\n📋 验证修复结果：")
idx = content.find('def resource_path')
if idx >= 0:
    end = content.find('\n\n', idx)
    if end == -1: end = idx + 300
    print(content[idx:end])
print(f"\n📌 import sys 出现次数：{content.count('import sys')}")
print(f"📌 import os 出现次数：{content.count('import os')}")
print(f"📌 setWindowIcon 调用数：{content.count('setWindowIcon')}")