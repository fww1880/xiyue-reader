import subprocess
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
# 恢复 HTTPS 地址
subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/fww1880/xiyue-reader.git'], cwd=base_dir)
print("""💡 老板，GitHub 在国内网络确实不太稳定，我建议用 **Gitee（码云）** 来托管代码！
Gitee 的好处：
✅ 国内访问飞快
✅ 同样支持 Pages 静态网站部署
✅ 和 GitHub 操作几乎一样
🔧 您需要做两步：
1️⃣ 访问 https://gitee.com 注册账号（如果有账号直接登录）
2️⃣ 创建仓库：登录后点右上角 "+" → 新建仓库
   - 仓库名：xiyue-reader
   - 路径：自动生成
   - 其他默认，点创建
3️⃣ 告诉我您 Gitee 的用户名，我来帮您配置推送！
或者如果您想继续用 GitHub，也可以：
- 配置代理（需要您告诉我代理地址）
- 或者换个网络环境再试
老板您选哪个方案？👨‍💼
""")