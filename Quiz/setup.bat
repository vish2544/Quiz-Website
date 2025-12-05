@echo off
REM AI Quiz Platform - Setup Script (Windows)
REM This script sets up the project for first-time run

echo.
echo ================================================
echo AI Quiz Platform - Setup Script
echo ================================================
echo.

REM Check if backend_py/.env exists
if not exist backend_py\.env (
    echo [1/3] Creating backend_py\.env from .env.example...
    copy backend_py\.env.example backend_py\.env
    echo ✓ Created backend_py\.env
) else (
    echo [1/3] backend_py\.env already exists
)

echo.
echo [2/3] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker not found! Please install Docker Desktop from https://docker.com
    exit /b 1
) else (
    echo ✓ Docker found
)

echo.
echo [3/3] Ready to start services
echo.
echo ================================================
echo NEXT STEPS:
echo ================================================
echo.
echo 1. Edit backend_py\.env with your secret keys (optional)
echo    - Update JWT_ACCESS_SECRET, JWT_REFRESH_SECRET, OTP_HMAC_SECRET
echo.
echo 2. Start Docker services:
echo    docker-compose up --build
echo.
echo 3. Open browser:
echo    http://localhost:3000
echo.
echo Frontend Entry Point:
echo    frontend/index.html
echo.
echo Backend Available At:
echo    http://localhost:4000
echo.
echo ================================================
echo Admin Credentials:
echo ================================================
echo Username: vish123
echo Password: 1914581
echo.
echo ================================================
echo.
pause
