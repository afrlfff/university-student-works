@echo off

if "%~1"=="" (
    echo Usage: %~nx0 ^<lab_number^>
    exit /b 1
)

cd /d "%~dp0lab-%~1" || exit /b 1

"C:\Program Files\CLIPS 6.3\Bin\CLIPSDOS.exe"