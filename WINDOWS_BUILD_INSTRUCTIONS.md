# 🪟 Windows Build Instructions

## 🚀 Super Simple - One Command

Open PowerShell in the `incident-copilot` folder and paste this:

```powershell
.\build.ps1
```

That's it! The script will:
1. ✅ Install all dependencies
2. ✅ Build the executable
3. ✅ Create `.env` template
4. ✅ Show you where the EXE is

**Result:** `dist\IncidentCopilot.exe`

---

## 🔧 Alternative - Manual Commands

If you prefer to run commands manually:

### Step 1: Install Dependencies
```powershell
pip install pyinstaller anthropic python-dotenv pydantic streamlit slack-sdk
```

### Step 2: Build Executable
```powershell
pyinstaller --onefile --windowed --name=IncidentCopilot --hidden-import=streamlit --hidden-import=anthropic --hidden-import=slack_sdk --collect-all=streamlit --collect-all=anthropic --noconfirm launcher.py
```

### Step 3: Find Your EXE
```powershell
cd dist
dir IncidentCopilot.exe
```

---

## 📦 Using the Executable

### Setup (First Time)

1. **Copy the EXE:**
   ```powershell
   Copy-Item "dist\IncidentCopilot.exe" "C:\YourFolder\"
   ```

2. **Create `.env` file** in the same folder:
   ```powershell
   cd C:\YourFolder
   notepad .env
   ```

3. **Add your API key:**
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

4. **Save and close** (Ctrl+S, then close Notepad)

5. **Double-click** `IncidentCopilot.exe`

Browser opens automatically! 🎉

---

## 📋 Quick Copy-Paste Examples

### Create .env file from PowerShell:
```powershell
@"
ANTHROPIC_API_KEY=sk-ant-your-key-here
"@ | Out-File -FilePath ".env" -Encoding UTF8
```

Then edit it:
```powershell
notepad .env
```

### Test if .env is correct:
```powershell
Get-Content .env
```

---

## 🐛 Troubleshooting

### "execution of scripts is disabled"
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "pip is not recognized"
Make sure Python is installed:
```powershell
python --version
```

If not installed, download from: https://www.python.org/downloads/

### Build takes too long
This is normal! The first build can take 5-10 minutes. Subsequent builds are faster.

### Executable is huge (300+ MB)
This is expected! It includes:
- Python runtime (~50 MB)
- Streamlit (~200 MB)
- All dependencies

---

## 🎯 Distribution

To share with others:

1. **Copy these files:**
   - `IncidentCopilot.exe`
   - `README.txt` (create one with setup instructions)

2. **Example README.txt:**
   ```
   IT Incident Copilot
   ===================

   Setup:
   1. Create a file named ".env" in this folder
   2. Open .env in Notepad and add:
      ANTHROPIC_API_KEY=your-key-here
   3. Get API key from: https://console.anthropic.com/
   4. Save and close
   5. Double-click IncidentCopilot.exe

   The app opens in your browser at http://localhost:8501
   ```

---

## 🔄 Rebuilding After Code Changes

If you update the Python code:

```powershell
# Clean old build
Remove-Item -Recurse -Force build, dist

# Rebuild
.\build.ps1
```

---

## 💾 File Sizes

Expect these sizes:
- `IncidentCopilot.exe`: ~280-350 MB (includes everything)
- `.env`: <1 KB (just text)
- Total distribution: ~300 MB

The size is large because it's a **fully standalone executable** with:
- Python 3.11 interpreter
- Streamlit web framework
- All Python libraries
- Your application code

No Python installation needed on target machines! 🎯

---

## ✅ Checklist

Before distributing:

- [ ] Build completed successfully
- [ ] EXE exists in `dist\` folder
- [ ] Tested EXE on your machine
- [ ] Created `.env` with your API key
- [ ] App opens in browser when you run it
- [ ] Report generation works
- [ ] Created README for end users

Ready to share! 🚀
