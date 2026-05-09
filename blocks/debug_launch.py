import os, sys, subprocess, time
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
print(f"📂 工作目录：{novel_reader_dir}")
print(f"📄 main.py 是否存在：{os.path.exists(main_file)}")
# 不关闭旧进程，直接在新窗口运行看报错
print("\n🚀 直接运行 main.py 看输出...")
result = subprocess.run(
    [sys.executable, main_file],
    cwd=novel_reader_dir,
    capture_output=True,
    text=True,
    timeout=5
)
print(f"\n📝 标准输出：{result.stdout}")
print(f"📝 错误输出：{result.stderr}")
print(f"📝 返回码：{result.returncode}")