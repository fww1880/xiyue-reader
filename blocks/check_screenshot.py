import os
screenshot_path = r'C:\Users\86139\Desktop\ScreenShot_2026-05-09_125408_068.png'
if os.path.exists(screenshot_path):
    print(f"✅ 图片存在")
    print(f"📏 大小：{os.path.getsize(screenshot_path)} bytes")
    print(f"📁 路径：{screenshot_path}")
else:
    print(f"❌ 图片不存在于该路径")
    # 搜索桌面上的截图
    desktop = r'C:\Users\86139\Desktop'
    for f in os.listdir(desktop):
        if 'ScreenShot' in f or '截图' in f:
            print(f"  找到：{f}")