import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
# 创建一个卡通书本图标（SVG格式，然后转成ico）
# 先创建SVG
book_svg = '''<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景圆形 -->
  <circle cx="128" cy="128" r="120" fill="#4A90E2"/>
  <!-- 书本主体 -->
  <rect x="60" y="80" width="136" height="110" rx="10" ry="10" fill="#F5F5DC"/>
  <!-- 书脊 -->
  <rect x="120" y="80" width="16" height="110" fill="#8B4513"/>
  <!-- 左侧页面阴影 -->
  <rect x="65" y="85" width="50" height="100" fill="#E8E8D0"/>
  <!-- 右侧页面 -->
  <rect x="140" y="85" width="50" height="100" fill="#FFFFE0"/>
  <!-- 书签 -->
  <path d="M 170 85 L 190 95 L 170 105 Z" fill="#FF6347"/>
  <!-- 书页线条 -->
  <line x1="75" y1="100" x2="105" y2="100" stroke="#D3D3D3" stroke-width="2"/>
  <line x1="75" y1="115" x2="105" y2="115" stroke="#D3D3D3" stroke-width="2"/>
  <line x1="75" y1="130" x2="105" y2="130" stroke="#D3D3D3" stroke-width="2"/>
  <line x1="75" y1="145" x2="105" y2="145" stroke="#D3D3D3" stroke-width="2"/>
  <line x1="75" y1="160" x2="105" y2="160" stroke="#D3D3D3" stroke-width="2"/>
  <!-- 右侧线条 -->
  <line x1="150" y1="100" x2="180" y2="100" stroke="#E0E0C0" stroke-width="2"/>
  <line x1="150" y1="115" x2="180" y2="115" stroke="#E0E0C0" stroke-width="2"/>
  <line x1="150" y1="130" x2="180" y2="130" stroke="#E0E0C0" stroke-width="2"/>
  <line x1="150" y1="145" x2="180" y2="145" stroke="#E0E0C0" stroke-width="2"/>
  <line x1="150" y1="160" x2="180" y2="160" stroke="#E0E0C0" stroke-width="2"/>
  <!-- 标题文字 -->
  <text x="128" y="220" font-size="24" text-anchor="middle" fill="white" font-weight="bold">喜阅</text>
</svg>'''
svg_path = os.path.join(novel_reader_dir, 'icon.svg')
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(book_svg)
print("✅ 已创建卡通书本SVG图标：icon.svg")
# 现在修改代码，设置窗口图标
# 需要使用QIcon
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查是否已经导入QIcon
if 'QIcon' not in content:
    # 在导入部分添加
    old_import = 'from PyQt5.QtWidgets import ('
    new_import = 'from PyQt5.QtWidgets import (\n    QIcon,'
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ 已添加 QIcon 导入")
    else:
        print("⚠️ 未找到导入位置")
# 在 setWindowTitle 后添加设置图标
old_setwindow = '''        self.setWindowTitle("喜阅")
        self.setMinimumSize(1200, 800)'''
new_setwindow = '''        self.setWindowTitle("喜阅")
        # 设置卡通书本图标
        import os
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.svg')
        if os.path.exists(icon_path):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(1200, 800)'''
if old_setwindow in content:
    content = content.replace(old_setwindow, new_setwindow)
    print("✅ 已添加窗口图标设置代码")
else:
    print("⚠️ 未找到精确匹配，尝试其他方式...")
    # 找 setWindowTitle 单独一行
    lines = content.split('\n')
    found = False
    for i, line in enumerate(lines):
        if 'self.setWindowTitle("喜阅")' in line:
            # 在这行之后插入图标代码
            lines.insert(i+1, '        # 设置卡通书本图标')
            lines.insert(i+2, '        import os')
            lines.insert(i+3, '        icon_path = os.path.join(os.path.dirname(__file__), \"icon.svg\")')
            lines.insert(i+4, '        if os.path.exists(icon_path):')
            lines.insert(i+5, '            from PyQt5.QtGui import QIcon')
            lines.insert(i+6, '            self.setWindowIcon(QIcon(icon_path))')
            content = '\n'.join(lines)
            found = True
            print("✅ 已插入图标代码")
            break
    if not found:
        print("❌ 未找到 setWindowTitle 行")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")