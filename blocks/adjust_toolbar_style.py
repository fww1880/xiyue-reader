import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找工具栏图标大小设置
old_size = "        toolbar.setIconSize(QSize(28, 28)) # 图标大一点"
new_size = "        toolbar.setIconSize(QSize(22, 22)) # 缩小一点更紧凑"
if old_size in content:
    content = content.replace(old_size, new_size)
    print("✅ 修改1：图标尺寸从 28×28 改为 22×22，按钮缩小了")
else:
    print("⚠️ 修改1：未找到图标尺寸设置行")
# 查找 QToolBar 的样式设置，添加立体按下效果
old_css_start = "            QToolBar {"
new_css = '''            QToolBar {
                spacing: 2px;
            }
            QToolButton {
                border: 1px solid #777;
                border-radius: 4px;
                background-color: #f0f0f0;
                padding: 2px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-color: #555;
            }
            QToolButton:pressed {
                background-color: #ccc;
                border: 1px inset #777;
                padding: 3px 1px 1px 3px;
            }
'''
# 替换原来的 QToolBar 块
if old_css_start in content:
    import re
    # 使用正则替换，找到 QToolBar 块的全部内容
    pattern = re.compile(r'(QToolBar\s*\{[^}]*\})', re.DOTALL)
    def replace_css(match):
        print("✅ 修改2：已更新 QToolBar 样式，添加立体按下效果")
        return new_css
    content = pattern.sub(replace_css, content, count=1)
else:
    print("⚠️ 修改2：未找到 QToolBar 样式块")
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