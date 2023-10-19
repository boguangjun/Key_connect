@echo off
setlocal enabledelayedexpansion

REM 指定你要安装 requests 库的 Python 解释器的路径
set python_path=Python310\python.exe

REM 在指定的 Python 解释器中使用 pip 安装 requests 库
%python_path% -m pip install Flask

endlocal