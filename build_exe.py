"""Build script for creating Windows executable of IT Incident Copilot."""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller."""

    # Get the absolute path to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # PyInstaller arguments
    args = [
        'launcher.py',                           # Main entry point
        '--name=IncidentCopilot',               # Name of the executable
        '--onefile',                             # Create a single executable
        '--windowed',                            # No console window (GUI mode)
        '--icon=NONE',                           # No icon (you can add one later)
        '--add-data=.streamlit;.streamlit',     # Include Streamlit config
        '--add-data=examples;examples',          # Include example files
        '--hidden-import=streamlit',
        '--hidden-import=anthropic',
        '--hidden-import=slack_sdk',
        '--hidden-import=pydantic',
        '--hidden-import=incident_parser',
        '--hidden-import=config',
        '--collect-all=streamlit',
        '--collect-all=anthropic',
        '--noconfirm',                          # Overwrite without asking
    ]

    # Add data files for different OS
    if sys.platform == 'win32':
        args.append('--add-data=.env.example;.')
    else:
        args.append('--add-data=.env.example:.')

    print("Building executable...")
    print(f"Arguments: {args}")

    PyInstaller.__main__.run(args)

    print("\n✅ Build complete!")
    print(f"Executable location: {script_dir}/dist/IncidentCopilot.exe")
    print("\nTo run: Double-click IncidentCopilot.exe or run from command line")

if __name__ == '__main__':
    build_exe()
