@echo off
setlocal

set python_executable=Python310\python.exe

:loop
echo *****************************���棺��Ҫ�Ҷ�daobiaomodel.bat********************************
echo ��ִ�еķ����б�
echo exit - �˳�
echo *****************************��ӭ����BC���������********************************
set /p input=�����뷨��: 


if "%input%"=="kongg" (
  set python_script=tools\kongg.py
rem ����û������Ƿ��� "exit"
) else if  "%input%"=="exit" (
  exit 0
) else (
  echo ��Ч��ָ�����������
)

REM ʹ�����õ� Python ������ִ�нű�
call %python_executable% %python_script%
call %python_executable% %python_script2%
call %python_executable% %python_script3%
call %python_executable% %python_script4%
call %python_executable% %python_script5%

rem ��� python_script �������ݣ��Ա�����һ��ѭ������ѡ��ű�
set "python_script="
set "python_script2="
set "python_script3="
set "python_script4="
set "python_script5="

goto loop