@echo off
setlocal

echo ExifTool by Mohsyn - Context Menu Installer
echo ==========================================

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

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo WARNING: Python is not found in PATH!
    echo Please make sure Python is installed and added to PATH.
    echo You can download Python from: https://python.org
    echo.
    pause
)

REM Check if required Python packages are installed
echo Checking Python dependencies...
python -c "import PIL, exifread" >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo WARNING: Required Python packages not found!
    echo Please install them by running:
    echo   pip install Pillow ExifRead
    echo.
    echo Would you like to install them now? (Y/N)
    set /p install_deps=
    if /i "%install_deps%"=="Y" (
        echo Installing dependencies...
        pip install Pillow ExifRead
        if %errorLevel% neq 0 (
            echo Failed to install dependencies!
            pause
            exit /b 1
        )
    ) else (
        echo Continuing without installing dependencies...
    )
)

REM Check if exiftool_v12.py exists in the same directory
if not exist "%~dp0exiftool.py" (
    echo.
    echo ERROR: exiftool.py not found in the same directory!
    echo Please make sure both files are in the same folder.
    echo.
    pause
    exit /b 1
)

REM Install the registry entries
echo.
echo Installing context menu entries...
if exist "%~dp0exiftool_context_menu.reg" (
    regedit /s "%~dp0exiftool_context_menu.reg"
    if %errorLevel% == 0 (
        echo Context menu entries installed successfully!
    ) else (
        echo Failed to install context menu entries!
        pause
        exit /b 1
    )
) else (
    echo ERROR: exiftool_context_menu.reg not found!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo You can now right-click on image files (.jpg, .jpeg, .png, .tiff, .tif)
echo and select "ExifTool by Mohsyn" to access the following options:
echo   * View MetaData    - Display metadata in a command window
echo   * Extract MetaData - Save metadata to separate files
echo   * Copy MetaData    - Copy metadata to clipboard (single files only)
echo.
echo Note: The command window will stay open after execution.
echo       Press any key in the window to close it.
echo.
pause