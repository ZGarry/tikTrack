# 上传PerfTrack到PyPI的步骤

## 准备工作

1. 确保安装了必要的工具

```bash
pip install setuptools wheel twine
```

2. 更新版本号

编辑`perftrack/__init__.py`文件中的版本号，每次上传新版本前都要更新。

## 构建包

在perftrack包的根目录（包含setup.py的那个目录）运行：

```bash
python setup.py sdist bdist_wheel
```

这将在`dist/`目录下创建源码分发包和wheel包。

## 测试上传到TestPyPI（可选但推荐）

首先上传到TestPyPI进行测试：

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

然后可以从TestPyPI安装测试：

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps perftrack
```

## 上传到正式PyPI

确认一切正常后，上传到正式PyPI：

```bash
twine upload dist/*
```

系统会要求输入PyPI的用户名和密码。

## 安装发布的包

现在可以通过pip安装您的包：

```bash
pip install perftrack
```

## 注意事项

- 确保每次上传前都更新版本号
- 如果您在上传后发现问题，无法在PyPI上删除已发布的文件，只能上传新版本
- 确保您的包名没有被其他人占用
- 确保README.md包含足够详细的使用说明

祝您成功！ 