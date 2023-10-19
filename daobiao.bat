@echo off
setlocal

set python_executable=Python310\python.exe

:loop
echo *****************************警告：不要乱动daobiaomodel.bat********************************
echo 可执行的法术列表：

REM 添加新命令
echo "更新bat文件内容"的指令是"rrbat"
echo "读表"的指令是"b"
echo "启动"的指令是"q"
echo exit - 退出
echo *****************************欢迎来到BC的奇幻世界********************************
set /p input=请输入法术: 


if "%input%"=="kongg" (
  set python_script=tools\kongg.py

REM 添加新命令
) else if "%input%"=="rrbat" (
  set python_script=tools\gengxinbat.py
  set python_script2=tools\kong1.py
  set python_script3=tools\kong2.py
  set python_script4=tools\kong3.py
  set python_script5=tools\kong4.py
) else if "%input%"=="b" (
  set python_script=tools\dubiao.py
  set python_script2=tools\kong1.py
  set python_script3=tools\kong2.py
  set python_script4=tools\kong3.py
  set python_script5=tools\kong4.py
) else if "%input%"=="q" (
  set python_script=app.py
  set python_script2=tools\kong1.py
  set python_script3=tools\kong2.py
  set python_script4=tools\kong3.py
  set python_script5=tools\kong4.py
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