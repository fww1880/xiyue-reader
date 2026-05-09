import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 查找并替换 setMinimumSize
old_code = "self.setMinimumSize(1200, 800)"
new_code = "self.setMinimumSize(400, 300)"  # 允许更小的尺寸，实现“随意”调整
if old_code in content:
    content = content.replace(old_code, new_code)
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已修改窗口最小尺寸限制为 400x300，现在可以自由拖拽边框调整大小了！")
else:
    print("❌ 未找到 setMinimumSize(1200, 800)")