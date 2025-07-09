
set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas
set INIDIR=%GAMEDIR%\Data\NVSE\plugins

set DEST=.\00_bare

copy /Y "%INIDIR%\nvse_stewie_tweaks.ini" "%DEST%\Stewie Tweaks\Data\NVSE\plugins\"

pause
