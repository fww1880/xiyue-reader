import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
print("🔍 检查窗口标志设置 (WindowFlags)：")
for i, line in enumerate(lines, 1):
    if 'FramelessWindowHint' in line or 'setWindowFlags' in line or 'setFixedSize' in line:
        print(f"L{i}: {line.strip()}")
print("\n🔍 检查是否实现了自定义边缘拖拽逻辑：")
for i, line in enumerate(lines, 1):
    if 'mouseMoveEvent' in line or 'mousePressEvent' in line or 'mouseReleaseEvent' in line or 'resizeEvent' in line:
        print(f"L{i}: {line.strip()}")