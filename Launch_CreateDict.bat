@echo off
setlocal
cd /d "%~dp0"

:: Check if 'uv' is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv is not installed. Installing now...
    set DO_NOT_TRACK=1
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo  Installation complete. Relaunch File...
    TIMEOUT /T 10
    set DO_NOT_TRACK=
    exit /b
)

:: Run 'uv run streamlit run main.py'
echo Running 'Create Dictionary App'...
uv run --with streamlit==1.43.2 --with pymupdf==1.25.4 streamlit run CreateDict.py --browser.gatherUsageStats=False --server.port=82 --theme.base="light" --theme.primaryColor="#57b431"

pause