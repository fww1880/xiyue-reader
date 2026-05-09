# 喜阅阅读器 - Android APK 打包指南
## 📱 项目说明
本项目已配置好 GitHub Actions 自动构建流程，可将 Python PyQt5 应用打包为 Android APK。
## 🚀 快速开始
### 步骤 1：创建 GitHub 仓库
1. 访问 https://github.com
2. 登录您的账号
3. 点击 "New" 创建新仓库
4. 仓库名建议为：`xiyue-reader` 或 `novel-reader`
5. **不要**勾选 "Initialize this repository with a README"
### 步骤 2：推送代码到 GitHub
在项目根目录打开命令行（PowerShell 或 CMD），执行：
```bash
# 初始化 Git 仓库
git init
# 添加所有文件
git add .
# 第一次提交
git commit -m "Initial commit: 喜阅阅读器"
# 关联远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/xiyue-reader.git
# 推送到 main 分支
git push -u origin main
```
如果遇到权限问题，可能需要先配置 Git：
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
### 步骤 3：触发自动构建
推送成功后，GitHub Actions 会自动开始构建！
1. 访问您的仓库页面
2. 点击顶部 "Actions" 标签
3. 您会看到 "Build Android APK" 工作流正在运行
4. 等待约 20-30 分钟，构建完成后会显示 ✅
### 步骤 4：下载 APK
构建成功后，有两种方式获取 APK：
**方式 A：从 Artifacts 下载（推荐）**
1. 在 Actions 页面点击最近的构建记录
2. 滚动到底部找到 "Artifacts" 区域
3. 点击 `xiyue-apk` 下载
4. 解压后得到 `.apk` 文件
**方式 B：从 Releases 下载（需要打标签）**
```bash
# 创建一个版本标签并推送
git tag v1.0.0
git push origin v1.0.0
```
这样会自动创建一个 Release，APK 会作为附件上传。
## 📋 构建配置说明
- **包名**: `org.novalreader.xiyue`
- **应用名**: 喜阅
- **最低 Android 版本**: API 21 (Android 5.0)
- **目标 Android 版本**: API 33 (Android 13)
- **架构**: arm64-v8a, armeabi-v7a
## ⚠️ 注意事项
1. **首次构建较慢**：需要下载 Android SDK、NDK 等工具链（约 10GB），耗时 20-30 分钟
2. **后续构建较快**：利用缓存后，约 10-15 分钟即可完成
3. **免费额度**：GitHub Actions 每月有 2000 分钟免费额度，足够个人使用
4. **签名证书**：当前生成的是 Debug 版本，可用于测试。如需发布，需配置正式签名
## 🛠️ 手动触发构建
如果需要重新构建或测试修改：
1. 进入仓库的 Actions 页面
2. 点击左侧 "Build Android APK"
3. 点击右上角 "Run workflow" 按钮
4. 选择分支（通常是 main）
5. 点击 "Run workflow"
## 📱 安装到手机
1. 将下载的 APK 文件传输到手机
2. 在手机设置中开启 "允许安装未知来源应用"
3. 点击 APK 文件进行安装
4. 享受阅读体验！
## 🔧 故障排查
**构建失败常见原因：**
- 依赖包不兼容 Android（如某些 Windows 专用库）
- 内存不足（GitHub Runner 默认 7GB RAM）
- 网络问题导致下载超时
**解决方案：**
- 检查 buildozer.spec 中的 requirements 列表
- 查看完整的构建日志定位错误
- 必要时拆分依赖或优化代码结构
## 📞 支持
如有问题，请在 GitHub Issues 中提问。
---
**祝使用愉快！** 🎉
