import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print("🔍 正在尝试捕获启动报错信息...")
try:
    # 运行并捕获输出
    result = subprocess.run(
        [sys.executable, main_file], 
        cwd=novel_reader_dir,
        capture_output=True, 
        text=True, 
        timeout=5  # 超时退出，因为我们只关心报错
    )
    if result.returncode != 0:
        print("❌ 发现报错信息：")
        print(result.stderr)
    else:
        print("✅ 启动正常（无报错输出）")
except subprocess.TimeoutExpired:
    print("✅ 程序运行中（未崩溃）")
except Exception as e:
    print(f"❌ 调试失败: {e}")