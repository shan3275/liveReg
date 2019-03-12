@echo off

:checkService
tasklist /FI "username eq administrator" | find /C "main.exe" > temp.txt
set /p num= < temp.txt
del /F temp.txt
if %num% == 2 ( goto checkMessage ) else ( goto restartService )



:checkMessage
echo %time% Program is running, 30 seconds later check again.. 
ping localhost -n 30> nul
goto checkService

:restartService
echo %time%
echo ********Program begin to start********
echo Program restart at %time%, pls check log >> restart_service.txt
start main.exe
REM set /p=.<nul 
set /p=.<nul
for /L %%i in (1 1 10) do set /p a=.<nul & ping.exe /n 2 127.0.0.1>nul
echo .
echo ********Program start complete********
goto checkService