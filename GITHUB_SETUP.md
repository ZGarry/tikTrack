# 将TikTrack上传到GitHub的步骤

## 1. 创建GitHub仓库

1. 登录您的GitHub账户
2. 点击右上角"+"图标，选择"New repository"
3. 填写仓库信息：
   - 仓库名称：`tiktrack`
   - 描述：`A simple performance tracking and visualization tool for Python applications`
   - 可见性：根据需要选择公开或私有
   - 初始化选项：不要选择任何初始化选项（因为我们已经有本地代码）
4. 点击"Create repository"按钮

## 2. 将本地仓库关联到GitHub

在命令行中，确保您位于tikTrack目录下，然后执行以下命令：

```bash
# 添加GitHub远程仓库（请替换为您的GitHub用户名）
git remote add origin https://github.com/您的用户名/tiktrack.git

# 将主分支重命名为main（现在的GitHub标准）
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

## 3. 验证上传

1. 刷新GitHub仓库页面
2. 您应该能看到所有文件已经上传
3. README.md文件内容将显示在仓库首页

## 4. 添加发布版本（可选）

如果您想在GitHub上标记发布版本：

1. 在GitHub仓库页面点击"Releases"
2. 点击"Create a new release"
3. 输入版本号（例如：v0.1.0）
4. 添加发布说明
5. 点击"Publish release"

## 5. 更新项目文档

更新README.md文件，添加GitHub仓库链接：

```markdown
# 安装

## 从PyPI安装
```bash
pip install tikTrack
```

## 从源代码安装
```bash
git clone https://github.com/您的用户名/tiktrack.git
cd tiktrack
pip install -e .
```
```

## 6. 后续维护

每次修改代码后：

```bash
git add .
git commit -m "描述您的更改"
git push
```

如果需要发布新版本，记得更新：
1. tiktrack/__init__.py中的版本号
2. 创建新的GitHub发布版本
3. 使用上传脚本将新版本上传到PyPI 