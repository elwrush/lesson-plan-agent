@echo off
REM This batch file reads the GEMINI_API_KEY from the registry and runs the image generation script
REM Usage: generate_image.bat "prompt" "output_path"

for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v GEMINI_API_KEY 2^>nul') do set GEMINI_API_KEY=%%b

if "%GEMINI_API_KEY%"=="" (
    echo Error: GEMINI_API_KEY not found in user environment variables
    exit /b 1
)

python scripts\generate_images_gemini.py %1 %2
