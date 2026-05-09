import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
result = subprocess.run(
    [sys.executable, '-m', 'py_compile', main_file],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("🎉 语法检查完全通过！没有任何错误了！")
else:
    print("❌ 还有错误：")
    print(result.stderr)