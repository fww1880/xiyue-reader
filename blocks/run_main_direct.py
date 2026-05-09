import os
import sys
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print(f"📁 切换到阅读器目录: {novel_reader_dir}")
sys.path.insert(0, novel_reader_dir)
try:
    # 直接执行main.py
    exec(open(main_file).read())
    print("✅ main.py执行完成")
except Exception as e:
    print(f"❌ 执行出错: {e}")
    import traceback
    traceback.print_exc()