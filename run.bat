@echo off
echo ========================================
echo Quiz AI Python - Flask Web Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak terinstall atau tidak ada di PATH
    echo Silakan install Python terlebih dahulu dari https://python.org
    pause
    exit /b 1
)

echo Python ditemukan!
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip tidak terinstall
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install Flask requests

if errorlevel 1 (
    echo ERROR: Gagal install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies berhasil diinstall!
echo.
echo ========================================
echo Starting Flask Application...
echo ========================================
echo.
echo Aplikasi akan berjalan di: http://localhost:5000
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

REM Start the Flask application
python app.py

pause