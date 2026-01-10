# IT Incident Copilot - Windows Executable Builder
# Copy this entire script and paste into PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IT Incident Copilot - EXE Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "ERROR: app.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the incident-copilot directory" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Step 1: Install PyInstaller and dependencies
Write-Host "[1/4] Installing build dependencies..." -ForegroundColor Yellow
pip install pyinstaller anthropic python-dotenv pydantic streamlit slack-sdk --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "Try running: pip install --upgrade pip" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "      Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Create launcher if it doesn't exist
Write-Host "[2/4] Checking launcher.py..." -ForegroundColor Yellow
if (Test-Path "launcher.py") {
    Write-Host "      launcher.py found!" -ForegroundColor Green
} else {
    Write-Host "      ERROR: launcher.py not found!" -ForegroundColor Red
    Write-Host "      Make sure all files are in the directory" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Step 3: Build the executable
Write-Host "[3/4] Building executable (this may take 5-10 minutes)..." -ForegroundColor Yellow
Write-Host "      Please be patient..." -ForegroundColor Gray
Write-Host ""

pyinstaller `
    --onefile `
    --windowed `
    --name=IncidentCopilot `
    --hidden-import=streamlit `
    --hidden-import=anthropic `
    --hidden-import=slack_sdk `
    --hidden-import=pydantic `
    --hidden-import=incident_parser `
    --hidden-import=config `
    --collect-all=streamlit `
    --collect-all=anthropic `
    --noconfirm `
    launcher.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "      Build completed successfully!" -ForegroundColor Green
Write-Host ""

# Step 4: Create .env template next to executable
Write-Host "[4/4] Creating .env template..." -ForegroundColor Yellow

$envTemplate = @"
# Claude API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Slack Configuration (Optional)
# SLACK_BOT_TOKEN=xoxb-your-bot-token
# SLACK_APP_TOKEN=xapp-your-app-token
"@

$envTemplate | Out-File -FilePath "dist\.env.example" -Encoding UTF8

Write-Host "      .env template created!" -ForegroundColor Green
Write-Host ""

# Success message
Write-Host "========================================" -ForegroundColor Green
Write-Host "         BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your executable is ready:" -ForegroundColor Cyan
Write-Host "  Location: " -NoNewline
Write-Host "dist\IncidentCopilot.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "To use it:" -ForegroundColor Cyan
Write-Host "  1. Copy 'dist\IncidentCopilot.exe' to any folder"
Write-Host "  2. Create a '.env' file in that folder with:"
Write-Host "     ANTHROPIC_API_KEY=sk-ant-your-actual-key" -ForegroundColor Gray
Write-Host "  3. Double-click IncidentCopilot.exe"
Write-Host ""
Write-Host "Get your API key from: https://console.anthropic.com/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
