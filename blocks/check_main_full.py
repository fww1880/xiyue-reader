import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"📝 main.py完整内容 ({len(content)} 字符)")
    print("=== 文件末尾 ===")
    lines = content.split('\n')
    for i in range(len(lines)-50, len(lines)):
        if i >= 0:
            print(f"{i+1}: {lines[i]}")
    print("\n=== 检查导入模块 ===")
    if "import PyQt5" in content:
        print("✅ 有PyQt5导入")
    else:
        print("❌ 没有PyQt5导入")
    if "import tkinter" in content:
        print("✅ 有tkinter导入")
    else:
        print("❌ 没有tkinter导入")