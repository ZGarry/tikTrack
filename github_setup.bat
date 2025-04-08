@echo off
echo TikTrack GitHub仓库设置助手
echo =========================
echo.

REM 检查是否设置了用户名和邮箱
git config --get user.name >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 您还没有设置Git用户名，请输入您的姓名：
    set /p USER_NAME=
    git config --global user.name "%USER_NAME%"
)

git config --get user.email >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 您还没有设置Git邮箱，请输入您的邮箱：
    set /p USER_EMAIL=
    git config --global user.email "%USER_EMAIL%"
)

echo.
echo 请输入您的GitHub用户名：
set /p GITHUB_USERNAME=

echo.
echo 将添加GitHub远程仓库...
git remote add origin https://github.com/%GITHUB_USERNAME%/tiktrack.git

echo.
echo 将主分支重命名为main（GitHub现在的标准）...
git branch -M main

echo.
echo 现在您需要先在GitHub上创建仓库。
echo 请访问: https://github.com/new
echo.
echo 创建新仓库，名称为 "tiktrack"，不要初始化任何文件
echo.
echo 创建完成后，按任意键继续...
pause >nul

echo.
echo 是否要现在推送代码到GitHub? (Y/N)
set /p CHOICE=
if /i "%CHOICE%"=="Y" (
    echo 正在推送代码到GitHub...
    git push -u origin main
    
    echo.
    if %ERRORLEVEL% EQU 0 (
        echo 推送成功！
        echo 您可以访问 https://github.com/%GITHUB_USERNAME%/tiktrack 查看您的仓库
        
        echo.
        echo 不要忘记更新README.md文件中的用户名占位符
        echo 将所有"您的用户名"替换为"%GITHUB_USERNAME%"
    ) else (
        echo 推送失败，请检查错误信息
    )
) else (
    echo.
    echo 稍后您可以手动推送代码：
    echo git push -u origin main
)

echo.
echo 完成！

pause 