@ECHO OFF
REM usage: append_system_path "path"
set CURR_DIR=%~dp0
set QEMU_DIR=%~dp0qemu-img\
SET Key="HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
FOR /F "usebackq tokens=2*" %%A IN (`REG QUERY %Key% /v PATH`) DO Set CurrPath=%%B
ECHO %CurrPath% > system_path_bak.txt
SETX PATH "%CurrPath%";%CURR_DIR%;%QEMU_DIR% /m