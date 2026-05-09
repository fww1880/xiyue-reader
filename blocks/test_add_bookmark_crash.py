import os, subprocess, time, psutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
exe_path = os.path.join(novel_reader_dir, 'dist', '喜阅.exe')
# 杀掉所有喜阅进程
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if '喜阅.exe' in proc.info.get('name', ''):
            proc.kill()
    except: pass
time.sleep(2)
# 启动程序
print("🚀 启动喜阅...")
proc = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(5)  # 等待启动
print("✅ 程序已启动")
# 模拟添加书签
print("\n🔍 检查代码逻辑...")
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找 add_bookmark 函数
import re
match = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    func_code = match.group()
    print(f"📄 add_bookmark 函数代码（前300字符）：\n{func_code[:300]}")
    # 检查关键代码
    if 'QMessageBox.warning' in func_code:
        print("✅ 有 QMessageBox.warning 检查")
    if 'hasattr(self, ' in func_code:
        print("✅ 有 hasattr 检查")
    if 'self.save_bookmarks()' in func_code:
        print("✅ 调用 save_bookmarks")
    if 'self.refresh_bookmark_list()' in func_code:
        print("✅ 调用 refresh_bookmark_list")
# 查找 save_bookmarks 函数
match_sv = re.search(r'def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_sv:
    sv_code = match_sv.group()
    print(f"\n📄 save_bookmarks 函数代码（前200字符）：\n{sv_code[:200]}")
    if 'hasattr(self, ' in sv_code:
        print("✅ save_bookmarks 有 hasattr 检查")
    if 'json.dump' in sv_code:
        print("✅ 使用 json.dump")
# 检查可能的错误
print("\n🔍 检查可能的错误点：")
# 1. refresh_bookmark_list 是否存在
if 'def refresh_bookmark_list(self):' in content:
    print("✅ refresh_bookmark_list 函数存在")
else:
    print("❌ refresh_bookmark_list 函数不存在！这是可能的闪退原因")
# 2. get_position_preview 是否存在
if 'def get_position_preview(self, pos):' in content:
    print("✅ get_position_preview 函数存在")
else:
    print("❌ get_position_preview 函数不存在！这也是可能的闪退原因")
# 3. QMessageBox 导入
if 'from PyQt5.QtWidgets import QMessageBox' in content:
    print("✅ QMessageBox 已导入")
else:
    print("❌ QMessageBox 未导入！")
# 4. datetime 导入
if 'from datetime import datetime' in content or 'import datetime' in content:
    print("✅ datetime 已导入")
else:
    print("❌ datetime 未导入！")
# 5. json 导入
if 'import json' in content:
    print("✅ json 已导入")
else:
    print("❌ json 未导入！")
# 检查完整的 add_bookmark 函数
print("\n📋 add_bookmark 完整函数：")
if match:
    print(func_code)
proc.kill()
print("\n🔍 总结可能闪退原因：")
print("1. refresh_bookmark_list 函数缺失")
print("2. get_position_preview 函数缺失")
print("3. 缺少必要的导入")
print("4. 函数内部其他错误")