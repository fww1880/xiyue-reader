import os, sys, subprocess
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
print("🔍 捕获闪退错误信息...")
result = subprocess.run(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    capture_output=True,
    text=True,
    timeout=5
)
if result.returncode != 0:
    print("❌ 运行时错误：")
    print(result.stderr)
else:
    print("✅ 运行正常")