@echo off

:: color section
set COLOR_GREEN=[32m>nul
set COLOR_YELLOW=[1;33m>nul
set COLOR_RESET=[0m>nul

title Build pack from many mods

:: you can change path of "MASTER" folder after "="
set SOURCE=00_bare

:: by default destination path is path of script directory itself
set DEST=.

:: you can change name of output folder after "=" (not recommend)
set PACK_NAME=%SOURCE%_pack

cls
echo.

echo %COLOR_GREEN%An archive of the following mods will be created%COLOR_RESET%:
echo.

dir /B /ON "%SOURCE%"

echo.
echo %COLOR_YELLOW%If you're sure the list is correct, just press any key to continue..%COLOR_RESET%
echo.
pause

:: delete previous pack's folder & archive. it'll help you avoid mistakes
IF EXIST "%DEST%\%PACK_NAME%" (rd /s /q "%DEST%\%PACK_NAME%")
IF EXIST "%DEST%\%PACK_NAME%.7z" (del /q "%DEST%\%PACK_NAME%.7z")

timeout 2

:: copy all mods into united folder
mkdir "%DEST%\%PACK_NAME%"
powershell -c "Copy-Item -Path '.\%SOURCE%\*\*\' -Destination '%DEST%\%PACK_NAME%' -Recurse -Force"


:: compress build into archive
.\7za.exe a -mx1 -sse -ssp -stl -y ".\%PACK_NAME%.7z" ".\%PACK_NAME%\*"

:: delete pack folder again (maybe ur indexing option is "on" ha?)
IF EXIST "%DEST%\%PACK_NAME%" (rd /s /q "%DEST%\%PACK_NAME%")