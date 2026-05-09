import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 add_bookmark 函数
print("🔍 查找当前的 add_bookmark 函数...")
match = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\Z)', content, re.DOTALL)
if match:
    func = match.group()
    print(f"函数长度：{len(func)}")
    print("\n完整代码:")
    print("="*60)
    print(func)
    print("="*60)
    # 显示前50个字符用于 Edit 工具的 old 参数
    print(f"\n前100字符：{func[:100]}")
else:
    print("❌ 未找到 add_bookmark 函数")
# 检查是否有备份
backup = os.path.join(novel_reader_dir, 'main.py.bak')
if os.path.exists(backup):
    print(f"\n✅ 备份文件存在：{backup}")
    with open(backup, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    # 从备份中获取原始函数
    match_backup = re.search(r'def add_bookmark\(self\):.*?(?=\n    def |\Z)', backup_content, re.DOTALL)
    if match_backup:
        original_func = match_backup.group()
        print(f"备份中的函数长度：{len(original_func)}")
        print(f"前100字符：{original_func[:100]}")