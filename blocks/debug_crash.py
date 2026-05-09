import os
import sys
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
# 直接运行一下看看错误信息
print("🔍 直接启动阅读器查看错误...")
sys.path.insert(0, novel_reader_dir)
try:
    # 读取代码
    with open(main_file, 'r', encoding='utf-8') as f:
        code = f.read()
    # 检查语法错误
    import ast
    ast.parse(code)
    print("✅ 语法没有问题")
    # 查找可能的错误
    # 检查 QDockWidget 的导入和使用
    if 'QDockWidget' in code:
        print("✅ QDockWidget 已经导入")
    else:
        print("❌ QDockWidget 未导入")
    # 检查 bookshelf_dock 是否初始化
    if 'self.bookshelf_dock = QDockWidget' in code:
        print("✅ bookshelf_dock 已初始化")
    else:
        print("❌ bookshelf_dock 未初始化")
    # 检查有没有未定义的变量
    # 运行看看错误
    exec(code[:5000])  # 只运行到 init 部分
except SyntaxError as e:
    print(f"❌ 语法错误：第 {e.lineno} 行")
    print(e.text)
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()