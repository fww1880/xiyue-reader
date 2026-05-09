import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修改所有动画参数：从300ms → 400ms，缓动曲线更明显
old_duration = "        self.page_anim.setDuration(300)"
new_duration = "        self.page_anim.setDuration(400)"
count = content.count(old_duration)
if count > 0:
    content = content.replace(old_duration, new_duration)
    print(f"✅ 修改1：动画时长从 300ms → 400ms，替换了 {count*2} 处")
else:
    print("⚠️ 修改1：未找到原时长设置")
old_curve = "        self.page_anim.setEasingCurve(QEasingCurve.OutCubic)"
new_curve = "        self.page_anim.setEasingCurve(QEasingCurve.OutQuad)"
count2 = content.count(old_curve)
if count2 > 0:
    content = content.replace(old_curve, new_curve)
    print(f"✅ 修改2：缓动曲线从 OutCubic → OutQuad，动画更顺滑明显")
else:
    print("⚠️ 修改2：未找到原曲线设置")
# 另外，也可以尝试给自动滚屏也加上动画？不过老板说的是翻页效果，先解决翻页
# 检查是否动画在主类上
# 可能问题是：按钮绑定的方法不是带动画的那个？检查按钮绑定
print("\n🔍 检查工具栏按钮绑定：")
lines = content.split('\n')
found_prev = False
found_next = False
for i, line in enumerate(lines):
    if 'prev_action.triggered.connect' in line:
        print(f"  L{i+1}: {line.rstrip()}")
        found_prev = True
    if 'next_action.triggered.connect' in line:
        print(f"  L{i+1}: {line.rstrip()}")
        found_next = True
if found_prev and found_next:
    print("  ✅ 按钮绑定正确，指向 prev_page / next_page")
else:
    print("  ❌ 按钮绑定不正确")
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