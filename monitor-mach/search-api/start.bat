@echo off
setlocal

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=py"
)

if not exist "logs" mkdir logs

%PYTHON% -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
