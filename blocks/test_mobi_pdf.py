import os
import sys
# 测试mobi库是否真的能用
print("测试MOBI库功能...")
try:
    import mobi
    print("✓ mobi库导入成功")
    # 检查mobi库的实际API
    print("检查mobi库的方法...")
    try:
        # 看看mobi库有什么方法
        print(f"mobi模块方法: {dir(mobi)}")
        # 尝试创建一个简单的测试
        test_file = "test.mobi"
        if os.path.exists(test_file):
            print("有测试文件，尝试打开...")
            # 看看mobi.open是否可用
            if hasattr(mobi, 'open'):
                print("✓ mobi.open方法存在")
            else:
                print("✗ mobi.open方法不存在")
        else:
            print("无测试文件")
    except Exception as e:
        print(f"检查mobi库出错: {e}")
except ImportError as e:
    print(f"✗ mobi库导入失败: {e}")
print("\n测试PDF库功能...")
try:
    from PyPDF2 import PdfReader
    print("✓ PyPDF2导入成功")
    # 检查PdfReader功能
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        print("有测试PDF文件")
    else:
        print("无测试PDF文件")
except ImportError as e:
    print(f"✗ PyPDF2导入失败: {e}")
utils.set_state(success=True)