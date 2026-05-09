import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 检查是否添加了翻页方法
print("🔍 检查翻页功能添加情况...")
if 'def keyboard_pagination' in content:
    print("✅ keyboard_pagination 已添加")
else:
    print("❌ keyboard_pagination 未找到")
if 'def prev_page' in content:
    print("✅ prev_page 已添加")
else:
    print("❌ prev_page 未找到")
if 'def next_page' in content:
    print("✅ next_page 已添加")
else:
    print("❌ next_page 未找到")
if 'def wheel_event' in content:
    print("✅ wheel_event 已添加")
else:
    print("❌ wheel_event 未找到")
if 'def toggle_auto_scroll' in content:
    print("✅ toggle_auto_scroll 已添加")
else:
    print("❌ toggle_auto_scroll 未找到")
# 重启阅读器
print("\n🚀 重启阅读器...")
import sys
import subprocess
try:
    process = subprocess.Popen([sys.executable, main_file], cwd=novel_reader_dir)
    print("✅ 阅读器已启动！请查看桌面窗口。")
except Exception as e:
    print(f"❌ 启动失败：{e}")