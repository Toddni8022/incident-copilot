"""Launcher script for IT Incident Copilot executable."""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def find_streamlit():
    """Find the streamlit executable."""
    # Try to import streamlit to verify it's available
    try:
        import streamlit
        streamlit_path = Path(streamlit.__file__).parent / "cli.py"
        return str(streamlit_path)
    except ImportError:
        return None

def launch_app():
    """Launch the Streamlit application."""

    # Get the directory where the script is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        app_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(app_dir)

    # Path to app.py
    app_path = os.path.join(app_dir, 'app.py')

    if not os.path.exists(app_path):
        print(f"Error: Could not find app.py at {app_path}")
        input("Press Enter to exit...")
        return 1

    # Check for .env file
    env_path = os.path.join(app_dir, '.env')
    if not os.path.exists(env_path):
        print("⚠️  Warning: No .env file found!")
        print(f"Please create a .env file at: {env_path}")
        print("\nExample .env content:")
        print("ANTHROPIC_API_KEY=sk-ant-your-key-here")
        print("\nGet your API key from: https://console.anthropic.com/")
        print("\nPress Enter to continue anyway (app will show error)...")
        input()

    print("🚀 Starting IT Incident Copilot...")
    print(f"   Working directory: {app_dir}")
    print(f"   Application: {app_path}")
    print("\n📌 The app will open in your browser automatically.")
    print("   If it doesn't, navigate to: http://localhost:8501")
    print("\n⚠️  To stop the application, close this window or press Ctrl+C")
    print("-" * 60)

    try:
        # Launch Streamlit using Python module
        process = subprocess.Popen(
            [sys.executable, '-m', 'streamlit', 'run', app_path,
             '--server.headless', 'true',
             '--browser.gatherUsageStats', 'false'],
            cwd=app_dir
        )

        # Wait a bit for the server to start
        time.sleep(3)

        # Open browser
        webbrowser.open('http://localhost:8501')

        # Wait for the process
        process.wait()

    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down...")
        process.terminate()
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(launch_app())
