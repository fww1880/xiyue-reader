from PIL import Image, ImageDraw
# 创建 256x256 的图标图像
size = (256, 256)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# 绘制书本形状（卡通风格）
# 书本封面（左侧）
cover_color = (255, 100, 100, 255)  # 红色封面
page_color = (255, 255, 255, 255)   # 白色书页
# 左封面
draw.rectangle([40, 60, 120, 200], fill=cover_color, outline=(200, 50, 50, 255), width=3)
# 右书页
draw.rectangle([120, 60, 200, 200], fill=page_color, outline=(200, 200, 200, 255), width=2)
# 书脊
draw.rectangle([115, 60, 125, 200], fill=(220, 80, 80, 255))
# 添加一些装饰细节（卡通感）
# 封面上的小星星
draw.polygon([(80, 100), (85, 110), (70, 110)], fill=(255, 255, 0, 255))
draw.polygon([(90, 130), (95, 140), (80, 140)], fill=(255, 255, 0, 255))
# 书页上的线条（模拟文字）
for i in range(130, 190, 10):
    draw.line([(130, i), (190, i)], fill=(200, 200, 200, 255), width=2)
# 保存为 .ico 格式（需要多尺寸）
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icon_path = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader\book_icon.ico'
# 先保存为 PNG 临时文件
temp_png = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader\book_icon_temp.png'
img.save(temp_png)
# 使用 PIL 保存为 ICO（需要安装 pillow）
img.save(icon_path, format='ICO', sizes=sizes)
# 清理临时文件
import os
if os.path.exists(temp_png):
    os.remove(temp_png)
print(f"✅ 卡通书本图标已生成：{icon_path}")
print("📚 图标包含多种尺寸，适用于不同场景")