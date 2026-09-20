@echo off
echo ========================================================
echo Pushing CarePulse Health App to GitHub:
echo https://github.com/prajapati-kamal/carepulse-health-app
echo ========================================================
cd /d "%~dp0"
git remote set-url origin https://github.com/prajapati-kamal/carepulse-health-app.git
git branch -M main
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code successfully pushed to GitHub!
) else (
    echo [ERROR] Push failed. If this is a private repo or first time, please sign in when prompted.
)
pause
