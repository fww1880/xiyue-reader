import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
dist_dir = os.path.join(novel_reader_dir, 'dist')
exe_file = os.path.join(dist_dir, '喜阅.exe')
if os.path.exists(exe_file):
    size_mb = os.path.getsize(exe_file) / (1024 * 1024)
    print(f"✅ 可执行文件已生成！")
    print(f"📁 位置：{exe_file}")
    print(f"📏 大小：{size_mb:.1f} MB")
    print(f"\n📂 dist 目录内容：")
    for f in os.listdir(dist_dir):
        f_path = os.path.join(dist_dir, f)
        if os.path.isfile(f_path):
            print(f"  📄 {f} ({os.path.getsize(f_path)/1024/1024:.1f} MB)")
else:
    print(f"❌ 未找到可执行文件")
    print(f"📂 dist 目录内容：{os.listdir(dist_dir) if os.path.exists(dist_dir) else '目录不存在'}")