import os, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
backup_file = os.path.join(novel_reader_dir, 'main.py.bak')
# 从备份恢复
if os.path.exists(backup_file):
    print("📥 从备份恢复 main.py...")
    shutil.copy(backup_file, main_file)
    print("✅ 恢复完成")
    # 验证
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'def add_bookmark(self):' in content:
        print("✅ add_bookmark 函数已恢复")
    else:
        print("❌ 恢复失败")
else:
    print("❌ 备份文件不存在")