@echo off
echo ========================================================
echo Starting CarePulse Health App with Live Public Cloudflare URL
echo ========================================================
start "" python app.py
timeout /t 3
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:5000
pause
