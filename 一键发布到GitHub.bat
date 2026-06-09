@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 玄品心决 · 一键发布到 GitHub

echo.
echo ========================================
echo   玄品心决 · 发布到公开仓库
echo ========================================
echo.

echo [编译] Markdown → HTML...
python build.py 2>build_err.txt
if %errorlevel% neq 0 (
    echo 编译失败，请检查 build_err.txt
    type build_err.txt
    del build_err.txt 2>nul
    pause
    exit /b 1
)
del build_err.txt 2>nul
echo.

echo [1/3] 尝试推送到 GitHub...
git push -u origin master 2>push_err.txt
if %errorlevel% equ 0 goto SUCCESS

findstr /C:"Repository not found" push_err.txt >nul
if %errorlevel% equ 0 goto CREATE_REPO

type push_err.txt
echo.
echo 推送失败，请把上方报错发给我
del push_err.txt 2>nul
pause
exit /b 1

:CREATE_REPO
del push_err.txt 2>nul
echo.
echo 远程仓库还不存在，需要先在网页上建一个（30 秒）：
echo.
echo   1. 即将打开 GitHub 新建仓库页面
echo   2. 仓库名填: xuanpin-site
echo   3. 选 Public（公开）
echo   4. 不要勾选 Add a README
echo   5. 点 Create repository
echo.
start https://github.com/new?name=xuanpin-site&visibility=public
pause
echo.
echo [2/3] 再次推送...
git push -u origin master
if %errorlevel% neq 0 (
    echo 推送仍失败。常见原因：
    echo   - 仓库名不是 xuanpin-site
    echo   - 没选 Public
    echo   - GitHub 账号不是 18ok
    pause
    exit /b 1
)

:SUCCESS
echo.
echo [3/3] 启用 GitHub Pages
echo.
echo 请浏览器打开下面链接，Source 选 GitHub Actions：
start https://github.com/18ok/xuanpin-site/settings/pages
echo   https://github.com/18ok/xuanpin-site/settings/pages
echo.
echo 然后打开 Actions 看 Deploy 是否绿色：
start https://github.com/18ok/xuanpin-site/actions
echo.
echo ========================================
echo   推送成功！
echo   网址: https://18ok.github.io/xuanpin-site/
echo   等 Actions 跑绿后（1～2 分钟）用手机打开
echo ========================================
echo.
pause
