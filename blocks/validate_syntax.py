import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print("🔍 语法检查：")
result = subprocess.run(
    [sys.executable, '-m', 'py_compile', main_file],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ 语法检查通过！")
else:
    print("❌ 语法错误：")
    print(result.stderr)