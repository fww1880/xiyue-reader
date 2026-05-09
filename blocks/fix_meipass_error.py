import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复 resource_path 函数，正确判断 _MEIPASS
correct_rp = '''
import sys
import os
def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    try:
        # PyInstaller 打包后会设置 _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境下使用脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
'''
# 替换原有的 resource_path 定义
old_rp_match = re.search(r'def resource_path\(.*?\):.*?return os\.path\.join\(.*?relative_path\)', content, re.DOTALL)
if old_rp_match:
    content = content.replace(old_rp_match.group(), correct_rp.strip())
    print("✅ resource_path 函数已修复：正确处理 _MEIPASS 判断")
else:
    # 直接搜索并替换整个函数
    content = re.sub(r'def resource_path\(.*?\).*?(?=\n\n|\ndef |\nclass |\Z)', correct_rp, content, flags=re.DOTALL)
    print("✅ resource_path 函数已全局替换")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")
# 验证
print("\n📋 验证修复后的 resource_path 定义：")
idx = content.find('def resource_path')
if idx >= 0:
    end = content.find('return', idx + 50) + 50
    print(content[idx:end])