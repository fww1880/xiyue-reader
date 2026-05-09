import os
# 项目根目录
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
spec_path = os.path.join(base_dir, 'buildozer.spec')
# Buildozer 配置内容
spec_content = '''[app]
# (str) Title of your application
title = 喜阅
package.name = xiyue
package.domain = org.novalreader
source.dir = ./novel_reader
source.include_exts = py,png,jpg,ico,pdf,txt
source.include_patterns = assets/*,images/*.png,*.ico
orientation = portrait
fullscreen = 0
# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3, pyqt5, fitz, PyMuPDF, os, sys
# (str) Android entry point, default is okay for your app
entrypoint = main:main
# (bool) Enable AndroidX support
android.enable_androidx = True
# (int) Target Android API, should be as high as possible.
android.api = 33
android.minapi = 21
android.ndk = 25b
[buildozer]
log_level = 2
warn_on_root = 1
'''
with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(spec_content)
print(f"✅ 已创建 buildozer.spec 配置文件：{spec_path}")