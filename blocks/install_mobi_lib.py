# 使用utils安装mobi解析库
result = utils.install_packages('mobi')
if result:
    print("✓ mobi库安装成功")
    utils.set_state(success=True)
else:
    print("✗ mobi库安装失败，尝试安装mobigen")
    # 尝试备选方案
    result2 = utils.install_packages('mobigen')
    if result2:
        print("✓ mobigen库安装成功")
        utils.set_state(success=True)
    else:
        print("✗ 所有MOBI库都安装失败")
        utils.set_state(success=False, error="MOBI库安装失败")