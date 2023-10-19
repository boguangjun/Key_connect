@echo off
setlocal

set python_executable=Python310\python.exe
set python_script=app.py
call %python_executable% %python_script%
