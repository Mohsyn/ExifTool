@echo off
setlocal

echo ExifTool by Mohsyn - Context Menu Uninstaller
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
echo This will remove the ExifTool context menu entries from Windows Explorer.
echo.
set /p confirm=Are you sure you want to continue? (Y/N): 

if /i not "%confirm%"=="Y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Removing context menu entries...

REM Remove registry entries for each file type
echo Removing .jpg entries...
reg delete "HKEY_CLASSES_ROOT\.jpg\shell\ExifTool" /f >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.jpg\shell\ExifTool" /f >nul 2>&1

echo Removing .jpeg entries...
reg delete "HKEY_CLASSES_ROOT\.jpeg\shell\ExifTool" /f >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.jpeg\shell\ExifTool" /f >nul 2>&1

echo Removing .png entries...
reg delete "HKEY_CLASSES_ROOT\.png\shell\ExifTool" /f >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.png\shell\ExifTool" /f >nul 2>&1

echo Removing .tiff entries...
reg delete "HKEY_CLASSES_ROOT\.tiff\shell\ExifTool" /f >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.tiff\shell\ExifTool" /f >nul 2>&1

echo Removing .tif entries...
reg delete "HKEY_CLASSES_ROOT\.tif\shell\ExifTool" /f >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.tif\shell\ExifTool" /f >nul 2>&1

echo Removing general entries...
reg delete "HKEY_CLASSES_ROOT\*\shell\ExifTool" /f >nul 2>&1

echo.
echo >> Context menu entries have been removed successfully!
echo.
echo The ExifTool context menu options will no longer appear
echo when you right-click on image files.
echo.
echo Note: You may need to restart Windows Explorer or reboot
echo       for the changes to take effect completely.
echo.
pause