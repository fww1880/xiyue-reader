import os, shutil
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
source_icon = r'E:\AiPyPro\fww\icon.png'
target_icon = os.path.join(novel_reader_dir, 'book_icon.ico')
# 检查源图标是否存在
if not os.path.exists(source_icon):
    print(f"❌ 源图标文件不存在：{source_icon}")
else:
    print(f"✅ 源图标文件存在：{source_icon}")
    # 检查源图标格式
    source_size = os.path.getsize(source_icon)
    print(f"源图标大小：{source_size} bytes")
    # 将 PNG 转换为 ICO
    try:
        # 先备份旧的图标
        if os.path.exists(target_icon):
            backup_path = target_icon + '.backup'
            shutil.copy(target_icon, backup_path)
            print(f"✅ 备份旧图标：{backup_path}")
        # 复制 PNG 文件
        shutil.copy(source_icon, target_icon)
        print(f"✅ 已将 PNG 图标复制到：{target_icon}")
        # 检查新图标大小
        new_size = os.path.getsize(target_icon)
        print(f"新图标大小：{new_size} bytes")
    except Exception as e:
        print(f"❌ 图标替换失败：{e}")