import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 1. 修复主窗口阴影导致无法拖动边框的问题
# 将阴影应用到内部容器而不是主窗口本身，保留系统原生边框和拖拽功能
old_shadow = """        # 设置主窗口阴影效果
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(33, 150, 243, 40))  # 淡蓝色阴影
        self.setGraphicsEffect(shadow)"""
new_shadow = """        # 设置主窗口阴影效果（应用到内部容器，保留系统原生边框拖拽功能）
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        # 创建一个主容器包裹阅读面板
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 留出阴影空间
        main_layout.addWidget(self.reading_panel)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(33, 150, 243, 40))  # 淡蓝色阴影
        main_container.setGraphicsEffect(shadow)
        
        # 将容器设为中央部件
        self.setCentralWidget(main_container)"""
if old_shadow in content:
    content = content.replace(old_shadow, new_shadow)
    print("✅ 已修复主窗口阴影设置，恢复原生边框拖拽功能")
else:
    print("⚠️ 未找到旧阴影代码，尝试按行替换...")
    # Fallback logic if exact match fails
    lines = content.split('\n')
    new_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        if '# 设置主窗口阴影效果' in line:
            skip_next = True
            new_lines.append(new_shadow)
            continue
        if skip_next:
            if 'self.setGraphicsEffect(shadow)' in line:
                skip_next = False
                continue
            if 'def ' in line and not skip_next: # End of block
                skip_next = False
            continue
        new_lines.append(line)
    content = '\n'.join(new_lines)
    print("✅ 按行替换阴影代码完成")
# 2. 添加书架与正文之间的分割线样式，使其可见且易于拖动
old_dock_style_end = """        QDockWidget::close-button:hover, QDockWidget::float-button:hover {
        background: #BBDEFB;
        }
        \"\"\")"""
new_dock_style_end = """        QDockWidget::close-button:hover, QDockWidget::float-button:hover {
        background: #BBDEFB;
        }
        \"\"\")
        
        # 设置主窗口分割线样式（书架与正文之间的拖动条）
        self.setStyleSheet(\"\"\"
            QMainWindow::separator {
                width: 5px;
                background: #BBDEFB;
                border-radius: 2px;
            }
            QMainWindow::separator:hover {
                background: #64B5F6;
            }
        \"\"\")"""
if old_dock_style_end in content:
    content = content.replace(old_dock_style_end, new_dock_style_end)
    print("✅ 已添加分割线样式，书架边框现在可见且易于拖动")
else:
    print("⚠️ 未找到旧样式结尾，尝试追加...")
    # Find the end of dock style and append
    if 'self.bookshelf_dock.setStyleSheet' in content:
        # Find the closing \"\"\") of dock style
        idx = content.find('self.bookshelf_dock.setStyleSheet')
        end_idx = content.find('""")', idx)
        if end_idx != -1:
            content = content[:end_idx+4] + """
        
        # 设置主窗口分割线样式
        self.setStyleSheet(\"\"\"
            QMainWindow::separator {
                width: 5px;
                background: #BBDEFB;
                border-radius: 2px;
            }
            QMainWindow::separator:hover {
                background: #64B5F6;
            }
        \"\"\")
""" + content[end_idx+4:]
            print("✅ 已追加分割线样式")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 修改已保存")