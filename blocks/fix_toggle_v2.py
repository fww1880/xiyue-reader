import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 精确匹配 toggle_auto_scroll 方法
old_toggle = '''    def toggle_auto_scroll(self, checked):
        """切换自动滚屏"""
        if checked:
            self.auto_scroll_enabled = True
            # 速度默认5，间隔根据速度调整
            interval = 100 - self.auto_scroll_speed * 8
            self.auto_scroll_timer.start(int(interval))
        else:
            self.auto_scroll_enabled = False
            self.auto_scroll_timer.stop()
            '''
new_toggle = '''    def toggle_auto_scroll(self, checked):
        """切换自动滚屏"""
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
            self.status_bar.showMessage("📜 滚屏已暂停", 3000)
            '''
if old_toggle in content:
    content = content.replace(old_toggle, new_toggle)
    print("✅ 修改2：滚屏切换优化成功！")
else:
    print("⚠️ 修改2：仍未匹配，检查精确内容...")
    # 打印实际内容看看
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def toggle_auto_scroll' in line:
            for j in range(i, i+12):
                if j < len(lines):
                    print(f"  L{j+1}: |{lines[j]}|")
            break
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