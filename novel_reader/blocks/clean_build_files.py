import os, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
# 清理 build 目录
build_dir = os.path.join(novel_reader_dir, 'build')
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print("✅ 已清理 build 目录")
# 清理 .spec 文件
for f in os.listdir(novel_reader_dir):
    if f.endswith('.spec'):
        os.remove(os.path.join(novel_reader_dir, f))
        print(f"✅ 已清理 {f}")
# 清理 __pycache__
pycache = os.path.join(novel_reader_dir, '__pycache__')
if os.path.exists(pycache):
    shutil.rmtree(pycache)
    print("✅ 已清理 __pycache__")
print("\n📁 最终 dist 目录：")
dist_dir = os.path.join(novel_reader_dir, 'dist')
for f in os.listdir(dist_dir):
    f_path = os.path.join(dist_dir, f)
    print(f"  📄 {f} ({os.path.getsize(f_path)/1024/1024:.1f} MB)")
print("\n🎉 打包完成！双击「喜阅.exe」即可直接运行！")