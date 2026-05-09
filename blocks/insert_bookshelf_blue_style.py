import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 找到 addDockWidget 这一行，在它后面插入样式
target_line = "        self.addDockWidget(Qt.LeftDockWidgetArea, self.bookshelf_dock)\n"
insert_index = -1
for i, line in enumerate(lines):
    if line.strip() == target_line.strip():
        insert_index = i + 1
        break
if insert_index != -1:
    style_code = """        # 设置书架蓝色调样式，无黑边
        self.bookshelf_dock.setStyleSheet(\"\"\"
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
        \"\"\")
"""
    lines.insert(insert_index, style_code)
    with open(main_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"✅ 已在 L{insert_index+1} 插入书架蓝色样式代码")
else:
    print("❌ 未找到 addDockWidget 行，无法插入样式")
# 验证语法
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")