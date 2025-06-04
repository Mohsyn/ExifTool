@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo PromptSniffer Context Menu Uninstaller
echo ============================================

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

echo.
echo This will remove PromptSniffer context menu entries from Windows Explorer.
echo.

echo Removing context menu entries...

echo Removing registry entries for HKEY_CLASSES_ROOT\*\shell\PromptSniffer
reg delete "HKCR\*\shell\PromptSniffer" /f

echo Remove registry entries for PromptSniffer commands in HKEY_LOCAL_MACHINE
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.view" /f
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.copy" /f
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.extract" /f
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\PromptSniffer.remove" /f
echo.
echo Registry entries removed successfully.
echo.
endlocal