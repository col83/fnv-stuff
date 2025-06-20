I don't know why this would be useful to anyone but me.  \(0_0)\

This repository contains scripts for creating standalone mod packages that should only be installed manually. Such as - "jip ln", "xnvse", "istewie tweaks" and similar mods.

Scripts work like this - at startup it recursive takes all files from a particular FOLDER with FOLDERS of mods and copies them into one united folder. Then the script calls the 7z archiver file and packs them (files) into an archive with the desired name.

The second script with the corresponding name does the following - just unpack the archive into the game folder.


 <h3>IMPORTANT:</h3>

The paths for taking files, their further moving and unpacking are specified by variables in these scripts. (I recommend installing the game as close to the root of the disk as possible and not in the system folder).

The default path for UNPACKING is - "%SYSTEMDRIVE%\Games\Fallout New Vegas"

The variable %SYSTEMDRIVE% means the PATH or the LETTER of the disk on which your operating system is installed!

This variable is a system variable.

You don't need to change this variable. It will be enough to change the path to the game directory after the first "/" symbol.