import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 导入 QPropertyAnimation
# 检查是否已导入
if 'QPropertyAnimation' not in content:
    # 在 from PyQt5.QtCore 那一行添加
    old_import = "from PyQt5.QtCore import Qt, QSettings, QTimer, QSize"
    new_import = "from PyQt5.QtCore import Qt, QSettings, QTimer, QSize, QPropertyAnimation, QEasingCurve"
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ 导入1：已添加 QPropertyAnimation, QEasingCurve")
    else:
        print("⚠️ 导入1：未找到导入行")
else:
    print("✅ 导入1：QPropertyAnimation 已存在")
# 替换所有 prev_page 方法（3个类中的）
# 使用通用模式：找到 prev_page 并替换
old_prev = '''    def prev_page(self):
        """上一页"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        scrollbar.setValue(current - page_size)'''
new_prev = '''    def prev_page(self):
        """上一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = max(0, current - page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(300)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.page_anim.start()'''
# 替换所有出现
count_prev = content.count(old_prev)
if count_prev > 0:
    content = content.replace(old_prev, new_prev)
    print(f"✅ 翻页1：已替换 {count_prev} 个 prev_page 方法，添加平滑动画")
else:
    print("⚠️ 翻页1：未找到 prev_page 方法")
# 替换所有 next_page 方法
old_next = '''    def next_page(self):
        """下一页"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        scrollbar.setValue(current + page_size)'''
new_next = '''    def next_page(self):
        """下一页（带平滑翻页动画）"""
        scrollbar = self.text_edit.verticalScrollBar()
        current = scrollbar.value()
        page_size = scrollbar.pageStep()
        target = min(scrollbar.maximum(), current + page_size)
        # 创建平滑滚动动画
        self.page_anim = QPropertyAnimation(scrollbar, b"value")
        self.page_anim.setDuration(300)
        self.page_anim.setStartValue(current)
        self.page_anim.setEndValue(target)
        self.page_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.page_anim.start()'''
count_next = content.count(old_next)
if count_next > 0:
    content = content.replace(old_next, new_next)
    print(f"✅ 翻页2：已替换 {count_next} 个 next_page 方法，添加平滑动画")
else:
    print("⚠️ 翻页2：未找到 next_page 方法")
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