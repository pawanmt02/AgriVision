@echo off
title AgriVision AI Launcher
echo ==========================================================
echo   AgriVision AI - Universal Crop Disease & Agronomy Engine
echo ==========================================================
echo.
echo [1/2] Starting Python FastAPI Backend on port 8005...
start "AgriVision Backend Core" cmd /k "cd /d %~dp0backend && python main.py"

timeout /t 2 /nobreak > nul

echo [2/2] Starting Next.js Frontend on port 3000...
start "AgriVision Frontend" cmd /k "cd /d %~dp0 && npm run dev"

echo.
echo Both services launched!
echo Frontend: http://localhost:3000
echo Backend API Docs: http://localhost:8005/docs
echo.
pause
