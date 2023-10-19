@echo off
setlocal

set python_executable=Python310\python.exe

:loop
echo *****************************警告：不要乱动daobiaomodel.bat********************************
echo 可执行的法术列表：
echo exit - 退出
echo *****************************欢迎来到BC的奇幻世界********************************
set /p input=请输入法术: 


if "%input%"=="kongg" (
  set python_script=tools\kongg.py
rem 检查用户输入是否是 "exit"
) else if  "%input%"=="exit" (
  exit 0
) else (
  echo 无效的指令，请重新输入
)

REM 使用设置的 Python 解释器执行脚本
call %python_executable% %python_script%
call %python_executable% %python_script2%
call %python_executable% %python_script3%
call %python_executable% %python_script4%
call %python_executable% %python_script5%

rem 清除 python_script 变量内容，以便在下一个循环重新选择脚本
set "python_script="
set "python_script2="
set "python_script3="
set "python_script4="
set "python_script5="

goto loop