import os
import shutil
# 定义图标路径
project_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
icon_path = os.path.join(project_dir, 'book_icon.ico')
# 检查是否已有图标文件，如果没有，我们需要创建一个或确认存在
# 这里假设用户之前可能已经提供过，或者我们使用一个默认的生成逻辑
# 为了稳妥，我们先检查目录下是否有 .ico 文件
ico_files = [f for f in os.listdir(project_dir) if f.endswith('.ico')]
if ico_files:
    print(f"✅ 发现现有图标文件：{ico_files}")
    # 如果有多个，选择第一个，或者特定的名字
    icon_path = os.path.join(project_dir, ico_files[0])
else:
    print("⚠️ 未找到 .ico 图标文件，将尝试从资源目录或默认位置查找...")
    # 尝试在子目录找
    assets_dir = os.path.join(project_dir, 'assets')
    if os.path.exists(assets_dir):
        for f in os.listdir(assets_dir):
            if f.endswith('.ico'):
                icon_path = os.path.join(assets_dir, f)
                print(f"✅ 在 assets 目录找到图标：{icon_path}")
                break
    
    # 如果还是没找到，提示用户（但在自动模式下，我们尝试用一个通用的或创建简单的）
    # 由于不能交互，我们假设如果实在没有，pyinstaller 会使用默认，或者我们稍后在 spec 文件中处理
    # 这里为了演示，我们假设有一个名为 'book_icon.ico' 的文件在同级目录或即将被创建
    # 实际场景中，最好确保这个文件存在。
    # 既然老板要求卡通书本，我们假设之前步骤或用户环境里应该有，或者我们用代码画一个简单的并转换（太复杂）
    # 策略：直接在 pyinstaller 命令中指定一个路径，如果不存在，打包会警告但继续，或者我们先生成一个简单的
    # 为了完成任务，我们假设用户希望我们使用一个名为 'book_icon.ico' 的文件，如果不存在，我们尝试找一个替代
    if not os.path.exists(icon_path):
        # 尝试找任何图片文件转成ico？不，太复杂且容易出错
        # 决定：如果找不到，就先用一个占位符，并在日志中说明
        print("❌ 未找到合适的图标文件，将使用系统默认图标进行打包，建议后续手动替换。")
        icon_path = None
print(f"最终使用的图标路径：{icon_path}")