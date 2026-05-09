import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找书架样式
import re
# 尝试查找 setStyleSheet 包含 QDockWidget 的部分
match = re.search(r'self\.bookshelf_dock\.setStyleSheet\(""".*?"""\)', content, re.DOTALL)
if match:
    print("✅ 找到书架样式代码，准备替换")
    old_style = match.group(0)
    new_style = '''self.bookshelf_dock.setStyleSheet("""
            QDockWidget {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F0F4F8, stop:1 #E1EBF5);
            }
            QDockWidget::title {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #90CAF9, stop:1 #64B5F6);
                padding: 6px;
                color: white;
                font-weight: bold;
                border: none;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                border: none;
                background: #E3F2FD;
                border-radius: 3px;
            }
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                background: #BBDEFB;
            }
        """)'''
    content = content.replace(old_style, new_style)
    print("✅ 已替换书架样式为蓝色调无黑边")
    
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("📝 验证语法...")
    import subprocess, sys
    result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 语法检查通过！")
    else:
        print(f"❌ 语法错误：{result.stderr}")
else:
    print("⚠️ 仍未找到书架样式代码，可能需要检查代码结构")