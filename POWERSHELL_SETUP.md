# ⚡ PowerShell Complete Setup

## 🚀 One Command Does Everything!

Open PowerShell in the `incident-copilot` folder and run:

```powershell
.\setup-and-build.ps1
```

**This script will:**
1. ✅ Check Python installation
2. ✅ Install all dependencies
3. ✅ Prompt for your Claude API key
4. ✅ Create .env file automatically
5. ✅ Build the executable
6. ✅ Create distribution package
7. ✅ Offer to run the app

**Result:** Everything set up and ready to use!

---

## 🎯 Advanced Options

### Run with API key parameter:
```powershell
.\setup-and-build.ps1 -ApiKey "sk-ant-your-actual-key"
```

### Skip the build (just setup):
```powershell
.\setup-and-build.ps1 -SkipBuild
```

### Build and run immediately:
```powershell
.\setup-and-build.ps1 -RunAfterBuild
```

### Combine options:
```powershell
.\setup-and-build.ps1 -ApiKey "sk-ant-your-key" -RunAfterBuild
```

---

## 📋 What Happens Step-by-Step

### The script will:

**Step 1:** Check if Python is installed
- If not found, tells you where to download it

**Step 2:** Check project files
- Verifies app.py, launcher.py exist

**Step 3:** Install dependencies
- pyinstaller, anthropic, streamlit, slack-sdk, etc.
- Shows progress for each package

**Step 4:** Get your API key
- Prompts you to enter it
- Validates the format (sk-ant-...)
- Creates .env file automatically

**Step 5:** Build executable (5-10 minutes)
- Creates dist/IncidentCopilot.exe
- Copies .env to dist folder
- Shows file size when done

**Step 6:** Create distribution package
- Adds README.txt for end users
- Everything ready to share

**Step 7:** Test setup
- Verifies all files are in place
- Shows summary of what was created

**Done!** Offers to run the app immediately

---

## 🎬 Example Output

```
========================================
  IT Incident Copilot Setup
========================================

[1/7] Checking project files...
  ✓ Project files found

[2/7] Checking Python installation...
  ✓ Python installed: Python 3.13.1

[3/7] Installing dependencies...
  Installing pyinstaller...
    ✓ pyinstaller
  Installing anthropic...
    ✓ anthropic
  [...]
  ✓ All dependencies installed

[4/7] Setting up API key...
Enter your Claude API key (or press Enter to skip):
Format: sk-ant-...
API Key: sk-ant-your-key-here
  ✓ API key saved to .env

[5/7] Building executable...
  This will take 5-10 minutes. Please be patient...
  ✓ Build completed successfully!
  ✓ .env copied to dist folder
  Executable size: 287.45 MB

[6/7] Creating distribution package...
  ✓ Created README.txt for end users
  ✓ Distribution package ready in 'dist' folder

[7/7] Testing setup...
  ✓ .env file configured with API key
  ✓ Executable ready at: dist\IncidentCopilot.exe

========================================
         Setup Complete!
========================================

What you have now:

  ✓ .env file configured
  ✓ Executable: dist\IncidentCopilot.exe
  ✓ README: dist\README.txt

Next Steps:

  2. Run the web app:
     python -m streamlit run app.py
     OR
     .\dist\IncidentCopilot.exe

  3. To distribute:
     Share the 'dist' folder contents
     Users just need the .exe and .env file!

Run the app now? (Y/N):
```

---

## 🐛 Troubleshooting

### "Cannot be loaded because running scripts is disabled"

Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again.

### "Python not found"

Install Python from: https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation!

After installing, restart PowerShell and try again.

### "pip not found"

Run:
```powershell
python -m ensurepip --upgrade
```

### Build fails with "Module not found"

Try:
```powershell
pip install --upgrade pip
.\setup-and-build.ps1
```

### Script runs but nothing happens

Make sure you're in the correct folder:
```powershell
cd C:\Users\toddn\documents\incident-copilot
.\setup-and-build.ps1
```

---

## 📁 What Gets Created

After running the script:

```
incident-copilot/
├── .env                          ← Your API key (created)
├── build/                        ← Build artifacts (temp)
├── dist/                         ← Distribution folder
│   ├── IncidentCopilot.exe      ← The executable!
│   ├── .env                      ← Copy of your .env
│   └── README.txt               ← User instructions
└── IncidentCopilot.spec         ← Build config
```

**To distribute:** Just share the `dist` folder!

---

## ⏩ Quick Commands Reference

```powershell
# Full setup (interactive)
.\setup-and-build.ps1

# Setup with API key
.\setup-and-build.ps1 -ApiKey "sk-ant-abc123"

# Just install dependencies, skip build
.\setup-and-build.ps1 -SkipBuild

# Setup and run immediately
.\setup-and-build.ps1 -RunAfterBuild

# Rebuild after code changes
Remove-Item -Recurse -Force build, dist
.\setup-and-build.ps1

# Just run the app (after setup)
python -m streamlit run app.py

# Run the executable
.\dist\IncidentCopilot.exe

# Edit your API key
notepad .env
```

---

## ✅ Success Checklist

After running the script, you should have:

- [ ] ✅ `.env` file with your API key
- [ ] ✅ `dist\IncidentCopilot.exe` (~300 MB)
- [ ] ✅ `dist\README.txt` for users
- [ ] ✅ No error messages
- [ ] ✅ App runs when you test it

If all checked, you're ready to go! 🎉

---

## 🎁 Bonus: Create Desktop Shortcut

```powershell
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\Incident Copilot.lnk")
$Shortcut.TargetPath = "$(Get-Location)\dist\IncidentCopilot.exe"
$Shortcut.WorkingDirectory = "$(Get-Location)\dist"
$Shortcut.Save()
Write-Host "Desktop shortcut created!" -ForegroundColor Green
```

Now you can launch from your desktop! 🚀
