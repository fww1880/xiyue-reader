import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查导入部分
print("🔍 检查导入模块...")
import_section = content[:content.find('class NovelReader')]
print(f"导入部分：\n{import_section}")
# 添加 json 导入
if 'import json' not in import_section:
    # 找到最后一个 import 语句
    last_import = re.search(r'^import .*?$|^from .*? import .*?$', import_section, re.MULTILINE)
    if last_import:
        end_pos = last_import.end()
        new_content = content[:end_pos] + '\nimport json' + content[end_pos:]
        print("✅ 在导入部分末尾添加 import json")
        content = new_content
    else:
        # 如果找不到，就在文件开头添加
        content = 'import json\n' + content
        print("✅ 在文件开头添加 import json")
# 检查 save_bookmarks 函数
print("\n🔍 检查 save_bookmarks 函数...")
match_sv = re.search(r'def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_sv:
    sv_code = match_sv.group()
    if 'import json' not in sv_code:
        print("✅ save_bookmarks 函数内没有 import json，依赖全局导入")
# 保存修改
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 修改已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ Python 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
# 验证
print("\n📋 验证导入：")
if 'import json' in content[:200]:
    print("✅ json 导入已添加")