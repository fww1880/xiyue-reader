[app]
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
