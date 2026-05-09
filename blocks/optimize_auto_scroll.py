import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 修改1: 优化 do_auto_scroll 方法，每次滚动更多像素 =====
old_scroll = """    def do_auto_scroll(self):
        \"\"\"执行自动滚屏\"\"\"
        scroll_bar = self.text_edit.verticalScrollBar()
        current_value = scroll_bar.value()
        scroll_bar.setValue(current_value + 1)"""
new_scroll = """    def do_auto_scroll(self):
        \"\"\"执行自动滚屏\"\"\"
        scroll_bar = self.text_edit.verticalScrollBar()
        current_value = scroll_bar.value()
        # 根据速度调节每次滚动像素数，实现平滑滚屏效果
        step = max(1, int(self.auto_scroll_speed / 10))
        scroll_bar.setValue(current_value + step)
        # 滚到底部时自动停止
        if current_value >= scroll_bar.maximum() - 10:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()
            self.auto_scroll_action.setChecked(False)
            self.status_bar.showMessage("📜 已滚到底部，滚屏结束", 3000)"""
if old_scroll in content:
    content = content.replace(old_scroll, new_scroll)
    print("✅ 修改1：滚屏效果优化，滚动更流畅且到底自动停止")
else:
    print("⚠️ 修改1：未找到 do_auto_scroll 方法")
# ===== 修改2: 优化 toggle_auto_scroll，增加速度调节和快捷键 =====
old_toggle = """    def toggle_auto_scroll(self, checked):
        \"\"\"切换自动滚屏\"\"\"
        if checked:
            self.auto_scroll_enabled = True
            interval = 100 - self.auto_scroll_speed * 8
            self.auto_scroll_timer.start(int(interval))
        else:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()"""
new_toggle = """    def toggle_auto_scroll(self, checked):
        \"\"\"切换自动滚屏\"\"\"
        if checked:
            self.auto_scroll_enabled = True
            # 速度值越大，间隔越小，滚动越快
            interval = max(10, 100 - self.auto_scroll_speed * 8)
            self.auto_scroll_timer.start(int(interval))
            self.auto_scroll_action.setText("⏸️ 暂停")
            self.status_bar.showMessage(f"📜 滚屏已开启（速度：{self.auto_scroll_speed}），点击暂停或按 Ctrl+Space 停止", 5000)
        else:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()
            self.auto_scroll_action.setText("📜 滚屏")
            self.status_bar.showMessage("📜 滚屏已暂停", 3000)"""
if old_toggle in content:
    content = content.replace(old_toggle, new_toggle)
    print("✅ 修改2：滚屏切换优化，按钮文字变化+状态提示")
else:
    print("⚠️ 修改2：未找到 toggle_auto_scroll 方法")
# ===== 修改3: 给滚屏按钮添加快捷键 Ctrl+Space =====
old_action = """        self.auto_scroll_action = QAction(\"📜 滚屏\", self)
        self.auto_scroll_action.setCheckable(True)
        self.auto_scroll_action.triggered.connect(self.toggle_auto_scroll)
        toolbar.addAction(self.auto_scroll_action)"""
new_action = """        self.auto_scroll_action = QAction(\"📜 滚屏\", self)
        self.auto_scroll_action.setCheckable(True)
        self.auto_scroll_action.setShortcut(\"Ctrl+Space\")
        self.auto_scroll_action.triggered.connect(self.toggle_auto_scroll)
        toolbar.addAction(self.auto_scroll_action)"""
if old_action in content:
    content = content.replace(old_action, new_action)
    print("✅ 修改3：滚屏按钮已添加快捷键 Ctrl+Space")
else:
    print("⚠️ 修改3：未找到滚屏按钮创建代码")
# ===== 修改4: 在工具栏增加速度调节按钮（加减速）=====
# 找到滚屏按钮后面的代码
old_speed = """        toolbar.addAction(self.auto_scroll_action)"""
new_speed = """        toolbar.addAction(self.auto_scroll_action)
        
        # 滚屏速度调节
        speed_down_action = QAction("🐢 减速", self)
        speed_down_action.triggered.connect(lambda: self.adjust_scroll_speed(-5))
        toolbar.addAction(speed_down_action)
        
        speed_up_action = QAction("🐇 加速", self)
        speed_up_action.triggered.connect(lambda: self.adjust_scroll_speed(5))
        toolbar.addAction(speed_up_action)"""
if old_speed in content:
    content = content.replace(old_speed, new_speed)
    print("✅ 修改4：已添加加减速按钮")
else:
    print("⚠️ 修改4：未找到插入位置")
# ===== 修改5: 添加 adjust_scroll_speed 方法 =====
# 在 toggle_auto_scroll 方法后面添加
lines = content.split('\n')
insert_pos = None
for i, line in enumerate(lines):
    if 'def toggle_auto_scroll' in line:
        for j in range(i+1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                insert_pos = j
                break
        break
speed_method = '''
    def adjust_scroll_speed(self, delta):
        """调整滚屏速度"""
        self.auto_scroll_speed = max(5, min(95, self.auto_scroll_speed + delta))
        self.settings.setValue('auto_scroll_speed', self.auto_scroll_speed)
        # 如果正在滚屏，动态调整速度
        if self.auto_scroll_enabled:
            interval = max(10, 100 - self.auto_scroll_speed * 8)
            self.auto_scroll_timer.setInterval(int(interval))
        direction = "⬆️ 加速" if delta > 0 else "⬇️ 减速"
        self.status_bar.showMessage(f"{direction} 当前滚屏速度：{self.auto_scroll_speed}", 3000)
'''
if insert_pos:
    lines.insert(insert_pos, speed_method)
    content = '\n'.join(lines)
    print(f"✅ 修改5：已添加 adjust_scroll_speed 方法")
else:
    print("⚠️ 修改5：未找到插入位置")
# 写入文件
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n📝 所有修改完成，正在验证语法...")
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'py_compile', main_file], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print(f"❌ 语法错误：{result.stderr}")