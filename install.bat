@echo off
setlocal EnableExtensions EnableDelayedExpansion
    echo.
    echo.
echo PromptSniffer by Mohsyn - Context Menu Installer
echo ================================================

REM Set the path to PromptSniffer.exe (modify this to your PromptSniffer installation path)
set "PromptSniffer_PATH=C:\PromptSniffer"
set "PromptSniffer_Exe=PromptSniffer.exe"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator... OK
) else (
    echo.
    echo ERROR: This script requires Administrator privileges!
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)


REM Get the active Python path and store in PYTHON_PATH variable
set "PYTHON_PATH="
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_PATH=%%i"

REM Check if PYTHON_PATH is set
if defined PYTHON_PATH (
    echo Active Python path is: %PYTHON_PATH%       ... OK
) else (
    echo Error: Python not found. Please ensure Python is installed and added to the system PATH.
    echo.
    exit /b 1)

if not defined PromptSniffer_path (
    echo Error: PromptSniffer_path environment variable is not defined.
    echo.
    exit /b 1)

echo.
echo This will install %PromptSniffer_Exe% context menu entries for image files in Windows Explorer.
echo.

if not exist %PromptSniffer_path% (
	echo Folder %PromptSniffer_path% does not exist. 
	echo It will be created and %PromptSniffer_Exe% will be copied there.
    echo if you wish to install in another location, 
	echo update target location in this batch file.
	echo To Cancel press Ctrl C or 
pause
    echo Creating directory: %PromptSniffer_path%
    echo.
    mkdir "%PromptSniffer_path%"
    if errorlevel 1 (
        echo Error: Failed to create directory %PromptSniffer_path%
    echo.
        exit /b 1))

if not exist %PromptSniffer_Exe% (
    echo Error: %PromptSniffer_Exe% not found in current directory.
    echo.
    exit /b 1 )

echo Copying %PromptSniffer_Exe% to %PromptSniffer_path%
copy "%PromptSniffer_Exe%" "%PromptSniffer_path%"
if errorlevel 1 (
    echo Error: Failed to copy %PromptSniffer_Exe% to %PromptSniffer_path%.
    exit /b 1 )

echo Successfully copied %PromptSniffer_Exe% to %PromptSniffer_path%.
echo.
if not exist "%PromptSniffer_PATH%" (
    echo ERROR: %PromptSniffer_PATH% not found
    pause
    exit /b 1
)
REM echo %promptsniffer_path%
set PromptSniffer_PATH=%PromptSniffer_PATH%\%PromptSniffer_Exe%

echo.
echo Installing context menu entries...
echo.

REM Create command store entries in HKEY_LOCAL_MACHINE
echo Creating command definitions...

echo Add registry entries for HKEY_CLASSES_ROOT\*\shell\PromptSniffer
reg add "HKCR\*\shell\PromptSniffer" /ve /f
reg delete "HKCR\*\shell\PromptSniffer" /ve /f
reg add "HKCR\*\shell\PromptSniffer" /v MUIVerb /t REG_SZ /d "PromptSniffer" /f
reg add "HKCR\*\shell\PromptSniffer" /v AppliesTo /t REG_SZ /d "System.FileName:\"*.png\" OR System.FileName:\"*.jpg\"  OR System.FileName:\"*.tif\" OR System.FileName:\"*.tiff\" OR System.FileName:\"*.jpeg\"" /f
reg add "HKCR\*\shell\PromptSniffer" /v SubCommands /t REG_SZ /d "PromptSniffer.view;PromptSniffer.copy;PromptSniffer.extract;PromptSniffer.remove" /f
    echo.
echo Add registry entries for PromptSniffer.view
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.view" /ve /t REG_SZ /d "View Metadata" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.view\command" /ve /t REG_SZ /d "\"cmd.exe\" \"/k\" \"%promptsniffer_path%\" \"%%1\"" /f
    echo.
echo Add registry entries for PromptSniffer.copy
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.copy" /ve /t REG_SZ /d "Copy Metadata to Clipboard" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.copy\command" /ve /t REG_SZ /d "\"%promptsniffer_path%\" \"--copy\" \"%%1\"" /f
    echo.
echo Add registry entries for PromptSniffer.extract
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.extract" /ve /t REG_SZ /d "Extract Metadata to file" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.extract\command" /ve /t REG_SZ /d "\"%promptsniffer_path%\" \"-s\" \"%%1\"" /f
    echo.
echo Add registry entries for PromptSniffer.remove
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.remove" /ve /t REG_SZ /d "Remove Metadata" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.remove\command" /ve /t REG_SZ /d "\"%promptsniffer_path%\" \"-r\" \"%%1\"" /f
    echo.
echo Registry entries added successfully.
echo.
echo To remove context menu just run uninstall.bat (it will not delete files, remove files manually to delete)
echo.
echo PromptSniffer by Mohsyn - Context Menu Installer
echo ================================================
    echo.

%promptsniffer_path% -h
echo off
endlocal