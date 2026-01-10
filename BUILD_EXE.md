# 📦 Building the Executable

This guide shows you how to create a standalone Windows executable (.exe) for the IT Incident Copilot.

## 🚀 Quick Build (Windows)

### Option 1: Using the Build Script (Easiest)

1. **Install build dependencies:**
   ```powershell
   pip install -r requirements-build.txt
   ```

2. **Run the build script:**
   ```powershell
   python build_exe.py
   ```

3. **Find your executable:**
   - Location: `dist/IncidentCopilot.exe`
   - Just double-click to run!

### Option 2: Manual Build

```powershell
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name=IncidentCopilot launcher.py --hidden-import=streamlit --hidden-import=anthropic --hidden-import=slack_sdk --collect-all=streamlit
```

---

## 📋 What Gets Packaged

The executable includes:
- ✅ Python interpreter
- ✅ All Python libraries (Streamlit, Anthropic, Slack SDK, etc.)
- ✅ Your application code (app.py, incident_parser.py, config.py, etc.)
- ✅ Example files

**NOT included (you need to provide):**
- ❌ `.env` file with your API keys (security - never bundle secrets!)

---

## 🎯 Using the Executable

### First Time Setup

1. **Copy the executable** from `dist/IncidentCopilot.exe` to wherever you want
2. **Create a `.env` file** in the same directory:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```
3. **Double-click** `IncidentCopilot.exe`
4. **Browser opens** automatically with the app!

### Directory Structure (After Build)

```
your-folder/
├── IncidentCopilot.exe    ← The executable
└── .env                    ← Your API keys (create this!)
```

---

## 🔧 Troubleshooting

### "Module not found" error
```powershell
pip install -r requirements-build.txt
python build_exe.py
```

### Executable is too large (300+ MB)
This is normal! It includes:
- Python interpreter (~50 MB)
- Streamlit framework (~200 MB)
- All dependencies

To reduce size, use `--onedir` instead of `--onefile`:
```powershell
pyinstaller --onedir --windowed --name=IncidentCopilot launcher.py
```

### Antivirus blocking the executable
- This is common with PyInstaller executables
- Add exception in your antivirus software
- Or distribute the Python script version instead

### App doesn't start
1. Check if `.env` file exists in the same folder as the .exe
2. Open Command Prompt and run: `IncidentCopilot.exe` to see error messages
3. Verify your `ANTHROPIC_API_KEY` is correct

---

## 📤 Distributing Your Executable

To share with others:

1. **Copy the executable:**
   - `dist/IncidentCopilot.exe`

2. **Create a README.txt** for users:
   ```
   IT Incident Copilot

   Setup:
   1. Create a file named ".env" (no extension) in this folder
   2. Add this line: ANTHROPIC_API_KEY=your-key-here
   3. Get API key from: https://console.anthropic.com/
   4. Double-click IncidentCopilot.exe

   The app will open in your browser automatically!
   ```

3. **Optional: Create a sample .env.example:**
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

---

## 🤖 Advanced: Including Slack Bot

If you want a real-time Slack bot (not just manual analysis), see the `slack_bot_realtime.py` file created separately.

---

## 💡 Tips

- **Testing**: Test the executable on a clean machine without Python installed
- **Updates**: Rebuild the executable when you update the code
- **Logs**: Check the console output if the executable fails to start
- **Size**: The first build is slow (~5 minutes), subsequent builds are faster

---

## 🐛 Known Issues

1. **Windows Defender SmartScreen**: May show warning on first run
   - Click "More info" → "Run anyway"
   - This happens because the executable isn't digitally signed

2. **Firewall**: May ask for network permissions (needed for API calls)
   - Allow access for the app to work

3. **Port 8501**: Make sure nothing else is using this port
   - Streamlit uses port 8501 by default
   - Close other instances before running

---

## 📞 Support

If you encounter issues:
1. Run the Python version directly: `python -m streamlit run app.py`
2. If that works but the .exe doesn't, it's a packaging issue
3. Check PyInstaller documentation: https://pyinstaller.org/
