import os, shutil, datetime
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
backup_root = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\backups'
# 创建备份目录
os.makedirs(backup_root, exist_ok=True)
# 生成时间戳
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_name = f"喜阅阅读器_备份_{timestamp}"
backup_path = os.path.join(backup_root, backup_name)
print(f"📦 开始保存项目快照...")
print(f"源目录：{novel_reader_dir}")
print(f"目标目录：{backup_path}")
# 复制整个项目目录（排除 dist 和 build，只保留源码）
shutil.copytree(
    novel_reader_dir, 
    backup_path, 
    ignore=shutil.ignore_patterns('dist', 'build', '__pycache__', '*.pyc')
)
print(f"\n✅ 项目已保存到：{backup_path}")
# 统计文件数
file_count = sum([len(files) for r, d, files in os.walk(backup_path)])
dir_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(backup_path) for filename in filenames)
print(f"📊 备份统计：")
print(f"  - 文件数量：{file_count} 个")
print(f"  - 总大小：{dir_size / (1024*1024):.2f} MB")
print(f"\n💡 提示：此备份包含所有源代码、图标文件和配置文件。")