import os
import re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 resource_path 定义
print("🔍 查找 resource_path 定义...")
# 修复参数定义错误（这个报错是因为调用时用了关键字参数，但定义时是位置参数，其实不对，报错提示说 unexpected keyword argument，说明调用错了）
# 看一下调用方式：resource_path('book_icon.ico') 是位置参数，定义应该没问题
# 可能是 resource_path 定义位置不对，或者函数定义有语法错误
# 先看 resource_path 定义
old_rp = '''
import sys
import os
def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
'''
# 重新替换为正确定义，确保没有语法错误
content = re.sub(r'def resource_path\(.*?\):.*?return os\.path\.join\(.*?\)', old_rp.strip(), content, flags=re.DOTALL)
# 检查调用
if "resource_path(relative_path='book_icon.ico')" in content:
    # 改成位置参数调用
    content = content.replace("resource_path(relative_path='book_icon.ico')", "resource_path('book_icon.ico')")
    print("✅ 已修复关键字参数调用错误")
# 检查是否有多余的括号
content = content.replace("self.setWindowIcon(QIcon(resource_path('book_icon.ico'))))", "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))")
print("✅ 已检查并修正多余括号")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修复已保存")
# 验证
print("\n📋 验证 resource_path 定义：")
idx = content.find('def resource_path')
if idx >= 0:
    end = content.find('\n', idx + 200)
    if end > 0:
        print(content[idx:end])