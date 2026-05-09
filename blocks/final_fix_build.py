import os, re, sys, subprocess, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
# 1. 修复 main.py
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
rp_func = '''
import sys
import os
def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
'''
# 清理旧的 resource_path 定义（防止重复或错误）
content = re.sub(r'def resource_path\(relative_path\):.*?return os\.path\.join\(os\.path\.abspath\("\."\), relative_path\)', rp_func.strip(), content, flags=re.DOTALL)
if 'def resource_path' not in content:
    idx = content.find('class ')
    if idx > 0:
        content = content[:idx] + rp_func + '\n' + content[idx:]
        print("✅ 已正确插入 resource_path 函数")
# 强制更新图标加载逻辑，直接调用避免变量作用域问题
content = re.sub(r'self\.setWindowIcon\(QIcon\([^)]+\)\)', "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))", content)
print("✅ 已更新 setWindowIcon 调用")
# 修复打开文件后的标题
content = re.sub(r'self\.setWindowTitle\(f"本地小说阅读器 - \{os\.path\.basename\(file_path\)\}"\)', 'self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")', content)
print("✅ 已统一窗口标题为「喜阅」")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 main.py 修改已保存")
# 2. 清理旧构建并重新打包
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
if os.path.exists(dist_dir): shutil.rmtree(dist_dir)
if os.path.exists(build_dir): shutil.rmtree(build_dir)
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",  # 关键：将图标打包进 exe 内部
    "--name=喜阅",
    main_file
]
print("🚀 开始重新打包（图标已深度嵌入）...")
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"🎨 窗口标题：喜阅")
        print(f"🎨 窗口图标：卡通书本（已修复路径映射）")
    else:
        print("❌ 打包完成但未找到 exe 文件")
else:
    print(f"❌ 打包失败：{res.stderr}")