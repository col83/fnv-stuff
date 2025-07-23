@echo off

SET VER=

SET COMPILE_FLAGS=--show-progress --jobs=8 --lto=no --static-libpython=no --assume-yes-for-downloads

SET IMPORTS=--enable-plugin=tk-inter

SET TYPE=--standalone --onefile --onefile-no-dll

SET OUTDIR=%USERPROFILE%\AppData\Local\Temp
SET OUTFILE=modpack-builder_v%VER%
SET OUT= --output-dir=%OUTDIR% --output-filename=%OUTFILE%

SET OPT=--windows-console-mode=disable --windows-uac-admin

SET ICON=--windows-icon-from-ico=./icon.ico

SET INCLUDE=--include-data-files=./7za.exe=7za.exe

SET METAINFO=--product-version="%VER%" --file-version="%VER%" --product-name="Modpack Builder" --company-name="dashi"

py -m nuitka %COMPILE_FLAGS% %IMPORTS% %TYPE% %OUT% %OPT% %ICON% %INCLUDE% %METAINFO% "./modpack-builder_v%VER%.pyw"

IF NOT EXIST ".\output" (md "output")

copy "%OUTDIR%\%OUTFILE%.exe" ".\output\"

.\output\%OUTFILE%.exe