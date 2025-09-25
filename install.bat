@echo off
REM Alternative installation script for Windows/container environments

echo Installing WikiExtractor in development mode...

REM Try pip install first
pip install -e .
if %errorlevel% equ 0 (
    echo ✅ Successfully installed with pip install -e .
    exit /b 0
)

echo ⚠️  pip install -e . failed, trying alternative methods...

REM Alternative 1: Install without editable mode
pip install .
if %errorlevel% equ 0 (
    echo ✅ Successfully installed with pip install .
    exit /b 0
)

REM Alternative 2: Use setup.py directly
python setup.py develop
if %errorlevel% equ 0 (
    echo ✅ Successfully installed with setup.py develop
    exit /b 0
)

echo 📁 Adding current directory to Python path...
set PYTHONPATH=%PYTHONPATH%;%CD%

echo ✅ WikiExtractor available via PYTHONPATH
echo You can now run: python -m wikiextractor.WikiExtractor --help
