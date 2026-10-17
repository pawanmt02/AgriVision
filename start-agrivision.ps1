# AgriVision AI Startup Script for PowerShell
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  AgriVision AI - Universal Crop Disease & Agronomy Engine" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$RootPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Python FastAPI Server
Write-Host "[1/2] Starting Python FastAPI Backend Core on port 8005..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\backend'; python main.py"

Start-Sleep -Seconds 2

# 2. Start Next.js PWA Frontend
Write-Host "[2/2] Starting Next.js Frontend on port 3000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\frontend'; npm run dev"

Write-Host "AgriVision AI is launching!" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:8005/docs" -ForegroundColor Yellow
Write-Host "Frontend App: http://localhost:3000" -ForegroundColor Yellow
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
