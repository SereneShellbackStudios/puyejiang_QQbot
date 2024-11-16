@echo off


REM 检查是否已设置PYTHON变量
IF "%PYTHON%"=="" (
    REM 如果没有设置PYTHON，则尝试使用系统默认的python或py命令
    python main.py
) ELSE (
    REM 如果设置了PYTHON，则使用指定的Python解释器
    %PYTHON% main.py
)

pause
