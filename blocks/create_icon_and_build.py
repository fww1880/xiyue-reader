import os
import sys
import subprocess
import shutil
import math
from PIL import Image, ImageDraw
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
icon_path = os.path.join(novel_reader_dir, 'book_icon.ico')
# 1. 生成高质量卡通书本图标
print("🎨 正在生成卡通书本图标...")
size = (256, 256)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# 颜色定义
cover_color = (74, 144, 226, 255)   # 柔和蓝封面
page_color = (245, 245, 245, 255)   # 白色书页
spine_color = (44, 94, 158, 255)    # 深蓝书脊
ribbon_color = (231, 76, 60, 255)   # 红色书签
star_color = (241, 196, 15, 255)    # 金色星星
outline_color = (30, 60, 90, 255)   # 深色轮廓
# 绘制书本主体 (圆角矩形)
draw.rounded_rectangle([40, 40, 216, 216], radius=12, fill=cover_color, outline=outline_color, width=4)
# 绘制书页
draw.rounded_rectangle([50, 45, 206, 211], radius=8, fill=page_color, outline=(200, 200, 200, 255), width=2)
# 绘制书脊
draw.rectangle([40, 40, 60, 216], fill=spine_color, outline=outline_color, width=2)
# 绘制书签带
draw.polygon([(110, 216), (130, 216), (130, 245), (120, 235), (110, 245)], fill=ribbon_color, outline=(180, 40, 40, 255), width=2)
# 绘制星星 (五角星)
cx, cy, r = 128, 130, 35
points = []
for i in range(5):
    angle = math.radians(i * 72 - 90)
    points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    angle = math.radians(i * 72 - 90 + 36)
    points.append((cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)))
draw.polygon(points, fill=star_color, outline=(200, 160, 0, 255), width=2)
# 保存多尺寸图标
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save(icon_path, format='ICO', sizes=sizes)
print(f"✅ 图标已生成：{icon_path}")
# 2. 修改 main.py
print("🔧 正在修改 main.py...")
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 添加 resource_path 函数
rp_func = '''
import sys
import os
def resource_path(relative_path):
    """获取资源文件的绝对路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
'''
if 'def resource_path' not in content:
    # 找到第一个 import 结束的位置，或者 class 定义之前
    idx = content.find('class ')
    if idx > 0:
        content = content[:idx] + rp_func + '\n' + content[idx:]
        print("✅ 已添加 resource_path 函数")
# 替换窗口图标设置
import re
# 替换 setWindowIcon 调用，直接使用 resource_path
content = re.sub(
    r'self\.setWindowIcon\(QIcon\([^)]+\)\)',
    "self.setWindowIcon(QIcon(resource_path('book_icon.ico')))",
    content
)
print("✅ 已更新 setWindowIcon 调用")
# 替换窗口标题设置
content = content.replace('self.setWindowTitle("喜阅")', 'self.setWindowTitle("喜阅")') # 保持默认
content = re.sub(
    r'self\.setWindowTitle\(f"本地小说阅读器 - \{os\.path\.basename\(file_path\)\}"\)',
    'self.setWindowTitle(f"喜阅 - {os.path.basename(file_path)}")',
    content
)
print("✅ 已统一窗口标题为「喜阅」")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 main.py 修改已保存")
# 3. 清理并重新打包
print("📦 开始重新打包...")
dist_dir = os.path.join(novel_reader_dir, 'dist')
build_dir = os.path.join(novel_reader_dir, 'build')
if os.path.exists(dist_dir): shutil.rmtree(dist_dir)
if os.path.exists(build_dir): shutil.rmtree(build_dir)
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--windowed",
    f"--icon={icon_path}",
    "--add-data=book_icon.ico;.",
    "--name=喜阅",
    main_file
]
res = subprocess.run(cmd, cwd=novel_reader_dir, capture_output=True, text=True, timeout=300)
if res.returncode == 0:
    exe = os.path.join(dist_dir, '喜阅.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"✅ 打包成功！")
        print(f"📦 路径：{exe}")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"🎨 窗口标题：喜阅")
        print(f"🎨 窗口图标：卡通书本（已深度嵌入）")
    else:
        print("❌ 打包完成但未找到 exe 文件")
else:
    print(f"❌ 打包失败：{res.stderr}")