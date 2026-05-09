import json, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 根据项目创建 package.json
# 项目是 Vue + Vite 小说阅读器
pkg = {
    "name": "xiyue-reader",
    "version": "1.0.0",
    "description": "Novel Reader - 支持 EPUB/TXT/PDF 小说阅读器",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    },
    "dependencies": {
        "vue": "^3.4.0",
        "epubjs": "^0.3.93",
        "pdfjs-dist": "^4.0.0"
    },
    "devDependencies": {
        "@vitejs/plugin-vue": "^5.0.0",
        "vite": "^5.0.0"
    }
}
pkg_path = os.path.join(base_dir, 'package.json')
with open(pkg_path, 'w', encoding='utf-8') as f:
    json.dump(pkg, f, indent=2, ensure_ascii=False)
print(f"✅ 已创建 package.json：{pkg_path}")
print("\n📋 内容：")
print(json.dumps(pkg, indent=2, ensure_ascii=False))