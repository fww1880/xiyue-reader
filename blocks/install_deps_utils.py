# 使用utils安装依赖
result = utils.install_packages('PyQt5', 'chardet', 'requests', 'beautifulsoup4', 'PyPDF2', 'lxml')
if result:
    print("✓ 所有依赖安装成功")
    utils.set_state(success=True)
else:
    print("✗ 部分依赖安装失败")
    utils.set_state(success=False, error="部分依赖安装失败")