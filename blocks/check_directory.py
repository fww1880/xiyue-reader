import os
import sys
import json
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
print(f"📁 阅读器目录: {novel_reader_dir}")
print(f"📁 目录是否存在: {os.path.exists(novel_reader_dir)}")
if os.path.exists(novel_reader_dir):
    print("📋 目录结构:")
    for item in os.listdir(novel_reader_dir):
        full_path = os.path.join(novel_reader_dir, item)
        if os.path.isdir(full_path):
            print(f"  📂 {item}")
        else:
            print(f"  📄 {item} - {os.path.getsize(full_path)} bytes")
    main_file = os.path.join(novel_reader_dir, 'main.py')
    if os.path.exists(main_file):
        print(f"\n✅ main.py存在，大小: {os.path.getsize(main_file)} bytes")
        # 预览前50行
        with open(main_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"\n📝 main.py前50行预览:")
            for i, line in enumerate(lines[:50]):
                print(f"  {i+1}: {line.strip()}")
    else:
        print(f"❌ main.py不存在")
else:
    print("❌ 阅读器目录不存在")