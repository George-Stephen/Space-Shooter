@echo off

:: Make the script to run as administrator automatically
if "%1"=="ELEV" (goto gotAdmin)
set "batchPath=%~0"
set "batchArgs=ELEV"
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPriv.vbs"
echo UAC.ShellExecute "%batchPath%", "%batchArgs%", "", "runas", 1 >> "%temp%\OEgetPriv.vbs"
"%temp%\OEgetPriv.vbs"


:: Change directory to the script's directory
cd /d %~dp0


:: Check if there is an environment already present, if there is one skip the command,else Create a virtual environment
if exist env (
    echo Virtual environment already exists. Skipping creation.
    venv\Scripts\activate
) else (
    echo Creating virtual environment...
    python -m venv env
    venv\Scripts\activate
    pip install -r requirements.txt
) 
:: Run the Python script
python "main.py"

:: Deactivate the virtual environment
deactivate

:: Pause the script
@REM REM Pause to keep the console window open
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 60819847d07c946ac621ba1e538d7784eb93460b
pause
goto :EOF

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/C %~s0 %*", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    goto :EOF
<<<<<<< HEAD
=======
@REM pause
@REM goto :EOF

@REM :UACPrompt
@REM     echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
@REM     echo UAC.ShellExecute "cmd.exe", "/C %~s0 %*", "", "runas", 1 >> "%temp%\getadmin.vbs"
@REM     "%temp%\getadmin.vbs"
@REM     del "%temp%\getadmin.vbs"
@REM     goto :EOF
>>>>>>> 555d6693377969c70d0e4e6ae962d582f69a2c26
=======
>>>>>>> 60819847d07c946ac621ba1e538d7784eb93460b
