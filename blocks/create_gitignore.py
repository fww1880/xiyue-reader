import os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
# Buildozer
.buildozer/
bin/
.apk
.cache/
# IDE
.vscode/
.idea/
*.swp
*.swo
*~
# OS
.DS_Store
Thumbs.db
# Backup
backups/
# Logs
*.log
'''
gitignore_path = os.path.join(base_dir, '.gitignore')
with open(gitignore_path, 'w', encoding='utf-8') as f:
    f.write(gitignore_content)
print(f"✅ 已创建 .gitignore 文件：{gitignore_path}")