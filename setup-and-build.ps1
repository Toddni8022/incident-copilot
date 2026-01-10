# ============================================
# IT Incident Copilot - Complete Setup Script
# ============================================
# This script does EVERYTHING:
# - Checks Python installation
# - Installs dependencies
# - Builds the executable
# - Creates .env file with your API key
# - Tests the installation
# ============================================

param(
    [string]$ApiKey = "",
    [switch]$SkipBuild,
    [switch]$RunAfterBuild
)

# Colors for output
function Write-Header {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Step, [string]$Message)
    Write-Host "[$Step] " -NoNewline -ForegroundColor Yellow
    Write-Host $Message
}

function Write-Success {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "  ✗ $Message" -ForegroundColor Red
}

# Main script starts here
Clear-Host
Write-Header "IT Incident Copilot Setup"

# Check if we're in the right directory
Write-Step "1/7" "Checking project files..."
if (-not (Test-Path "app.py") -or -not (Test-Path "launcher.py")) {
    Write-Error-Message "Project files not found!"
    Write-Host "`nPlease run this script from the incident-copilot directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Success "Project files found"

# Check Python installation
Write-Step "2/7" "Checking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python installed: $pythonVersion"
} catch {
    Write-Error-Message "Python not found!"
    Write-Host "`nPlease install Python 3.11+ from: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    pause
    exit 1
}

# Check pip
try {
    $pipVersion = pip --version 2>&1
    Write-Success "pip is available"
} catch {
    Write-Error-Message "pip not found!"
    Write-Host "`nTry running: python -m ensurepip --upgrade" -ForegroundColor Yellow
    pause
    exit 1
}

# Install/upgrade dependencies
Write-Step "3/7" "Installing dependencies..."
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "pyinstaller",
    "anthropic",
    "python-dotenv",
    "pydantic",
    "streamlit",
    "slack-sdk"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet --upgrade 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ $package" -ForegroundColor Green
    } else {
        Write-Host "    ✗ $package failed" -ForegroundColor Red
    }
}
Write-Success "All dependencies installed"

# Get API key
Write-Step "4/7" "Setting up API key..."
if ($ApiKey -eq "") {
    Write-Host "`nYou need a Claude API key from: " -NoNewline
    Write-Host "https://console.anthropic.com/" -ForegroundColor Cyan
    Write-Host "`nEnter your Claude API key (or press Enter to skip):" -ForegroundColor Yellow
    Write-Host "Format: sk-ant-..." -ForegroundColor Gray
    $ApiKey = Read-Host "API Key"
}

if ($ApiKey -ne "" -and $ApiKey -match "^sk-ant-") {
    # Create .env file in project root
    $envContent = @"
# Claude API Configuration
ANTHROPIC_API_KEY=$ApiKey

# Slack Configuration (Optional)
# SLACK_BOT_TOKEN=xoxb-your-bot-token
# SLACK_APP_TOKEN=xapp-your-app-token

# Optional Configuration
# MODEL=claude-3-5-sonnet-20241022
# TEMPERATURE=0.3
# MAX_TOKENS=4096
# LOG_LEVEL=INFO
"@
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Success "API key saved to .env"
} elseif ($ApiKey -ne "") {
    Write-Error-Message "Invalid API key format. Should start with 'sk-ant-'"
    Write-Host "  You can add it manually later to .env file" -ForegroundColor Yellow
} else {
    Write-Host "  Skipped - you can add it manually later to .env file" -ForegroundColor Yellow
}

# Build executable (unless skipped)
if (-not $SkipBuild) {
    Write-Step "5/7" "Building executable..."
    Write-Host "  This will take 5-10 minutes. Please be patient..." -ForegroundColor Gray
    Write-Host ""

    # Clean old builds
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" 2>$null }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" 2>$null }
    if (Test-Path "*.spec") { Remove-Item -Force "*.spec" 2>$null }

    # Build with PyInstaller
    $buildArgs = @(
        '--onefile',
        '--windowed',
        '--name=IncidentCopilot',
        '--hidden-import=streamlit',
        '--hidden-import=anthropic',
        '--hidden-import=slack_sdk',
        '--hidden-import=pydantic',
        '--hidden-import=incident_parser',
        '--hidden-import=config',
        '--collect-all=streamlit',
        '--collect-all=anthropic',
        '--noconfirm',
        'launcher.py'
    )

    pyinstaller $buildArgs

    if ($LASTEXITCODE -eq 0 -and (Test-Path "dist\IncidentCopilot.exe")) {
        Write-Success "Build completed successfully!"

        # Copy .env to dist folder
        if (Test-Path ".env") {
            Copy-Item ".env" "dist\.env"
            Write-Success ".env copied to dist folder"
        } else {
            # Create template in dist
            $envTemplate = @"
# Claude API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Slack Configuration (Optional)
# SLACK_BOT_TOKEN=xoxb-your-bot-token
"@
            $envTemplate | Out-File -FilePath "dist\.env.example" -Encoding UTF8
        }

        # Get file size
        $exeSize = [math]::Round((Get-Item "dist\IncidentCopilot.exe").Length / 1MB, 2)
        Write-Host "  Executable size: $exeSize MB" -ForegroundColor Gray
    } else {
        Write-Error-Message "Build failed!"
        Write-Host "`nCheck the error messages above" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Step "5/7" "Skipping build (--SkipBuild flag used)"
}

# Create distribution package
Write-Step "6/7" "Creating distribution package..."

if (Test-Path "dist\IncidentCopilot.exe") {
    # Create README for end users
    $readmeContent = @"
IT Incident Copilot
===================

QUICK START
-----------
1. Make sure the .env file is in this folder
2. Open .env and add your Claude API key:
   ANTHROPIC_API_KEY=sk-ant-your-actual-key
3. Save and close
4. Double-click IncidentCopilot.exe
5. Your browser will open automatically!

GET API KEY
-----------
Visit: https://console.anthropic.com/
Sign up and create an API key

TROUBLESHOOTING
---------------
- Windows Defender warning? Click "More info" > "Run anyway"
- Firewall prompt? Allow access (needed for API calls)
- Port 8501 in use? Close other instances first

SUPPORT
-------
For issues, visit: https://github.com/Toddni8022/incident-copilot

Enjoy your AI-powered incident reports!
"@
    $readmeContent | Out-File -FilePath "dist\README.txt" -Encoding UTF8
    Write-Success "Created README.txt for end users"
    Write-Success "Distribution package ready in 'dist' folder"
} else {
    Write-Host "  No executable to package" -ForegroundColor Yellow
}

# Test the setup
Write-Step "7/7" "Testing setup..."

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "ANTHROPIC_API_KEY=sk-ant-") {
        Write-Success ".env file configured with API key"
    } else {
        Write-Host "  .env file exists but API key not set" -ForegroundColor Yellow
    }
} else {
    Write-Host "  .env file not created (skipped by user)" -ForegroundColor Yellow
}

if (Test-Path "dist\IncidentCopilot.exe") {
    Write-Success "Executable ready at: dist\IncidentCopilot.exe"
}

# Summary
Write-Header "Setup Complete!"

Write-Host "What you have now:" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".env") {
    Write-Host "  ✓ .env file configured" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .env file - create manually" -ForegroundColor Yellow
}

if (Test-Path "dist\IncidentCopilot.exe") {
    Write-Host "  ✓ Executable: dist\IncidentCopilot.exe" -ForegroundColor Green
    Write-Host "  ✓ README: dist\README.txt" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Executable not built" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".env") -or -not ((Get-Content ".env" -Raw) -match "sk-ant-")) {
    Write-Host "  1. Edit .env file and add your API key:" -ForegroundColor Yellow
    Write-Host "     notepad .env" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "  2. Run the web app:" -ForegroundColor Yellow
Write-Host "     python -m streamlit run app.py" -ForegroundColor Gray
Write-Host "     OR" -ForegroundColor Gray
Write-Host "     .\dist\IncidentCopilot.exe" -ForegroundColor Gray
Write-Host ""

Write-Host "  3. To distribute:" -ForegroundColor Yellow
Write-Host "     Share the 'dist' folder contents" -ForegroundColor Gray
Write-Host "     Users just need the .exe and .env file!" -ForegroundColor Gray
Write-Host ""

# Offer to run
if ($RunAfterBuild -and (Test-Path ".env") -and ((Get-Content ".env" -Raw) -match "sk-ant-")) {
    Write-Host "Starting the application..." -ForegroundColor Green
    python -m streamlit run app.py
} elseif (-not $RunAfterBuild) {
    Write-Host "Run the app now? (Y/N): " -NoNewline -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host "`nStarting Streamlit app..." -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Gray
        python -m streamlit run app.py
    }
}

Write-Host ""
Write-Host "Thank you for using IT Incident Copilot! 🚨" -ForegroundColor Cyan
Write-Host ""
