[app]
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
