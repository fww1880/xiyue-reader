import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
spec_path = os.path.join(base_dir, 'buildozer.spec')
print("🛠️ 重新配置 buildozer.spec 文件...")
# 创建正确的 buildozer.spec 配置
correct_spec = """[app]
# (str) Title of your application
title = 喜阅阅读器
package.name = xiyue
package.domain = org.novalreader
source.dir = .
source.include_exts = py,vue,js,html,css,json,png,jpg,ico,pdf,txt
source.include_pattern = assets/*,src/*,*.html,*.js,*.json,*.vue,*.css
# (list) Application requirements
requirements = python3,kivy,kivymd,pillow,requests,chardet,epubjs,jsdom,canvas,webpack
# (str) Application version
version = 1.0.0
# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
# (int) Android API to use
android.api = 33
# (str) Android NDK version to use
android.ndk = 25.2.9519653
# (str) Android SDK version to use
android.sdk = 33.0.2
# (list) Android activities
android.activities = MainActivity
# (str) Orientation
orientation = portrait
# (bool) Fullscreen
fullscreen = false
[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
"""
with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(correct_spec)
print("✅ buildozer.spec 已重新配置！")
print("📋 关键改进：")
print("- source.dir = . (当前目录)")
print("- 包含 vue, js, html, css 等前端文件类型")
print("- 指定了正确的 Python 依赖")
print("- 配置了 Android API 33 和 NDK")
import subprocess
print("\n🚀 提交并推送...")
subprocess.run(['git', 'add', spec_path], cwd=base_dir, capture_output=True)
res = subprocess.run(['git', 'commit', '-m', 'Fix: update buildozer.spec for Vue project'], cwd=base_dir, capture_output=True, text=True)
print(f"Commit: {res.stdout.strip()}")
push = subprocess.run(['git', 'push'], cwd=base_dir, capture_output=True, text=True)
if push.returncode == 0:
    print("\n🎉 修复已推送！GitHub Action 将自动重新运行！")
    print("🔗 查看进度: https://github.com/fww1880/xiyue-reader/actions")
else:
    print(f"\n⚠️ 推送失败: {push.stderr}")