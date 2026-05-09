import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print("🔍 运行捕获错误...")
result = subprocess.run(
    [sys.executable, main_file],
    capture_output=True,
    text=True,
    timeout=5
)
if result.returncode != 0:
    print("❌ 错误输出：")
    print(result.stderr)
else:
    print("✅ 正常输出：")
    print(result.stdout)