"""
Simple installer for Sinhala TTS System
Creates desktop shortcut and installs dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def create_desktop_shortcut():
    """Create desktop shortcut on Windows"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Sinhala TTS.lnk")
        target = os.path.join(os.getcwd(), "sinhala_tts_app.py")
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✓ Desktop shortcut created")
        return True
        
    except ImportError:
        print("⚠ winshell not available, skipping desktop shortcut")
        return False
    except Exception as e:
        print(f"⚠ Could not create desktop shortcut: {e}")
        return False

def main():
    """Main installer function"""
    print("=" * 60)
    print("Sinhala TTS System Installer")
    print("=" * 60)
    
    # Install dependencies
    print("\n1. Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
        print("✓ Dependencies installed")
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return
    
    # Create desktop shortcut
    print("\n2. Creating desktop shortcut...")
    create_desktop_shortcut()
    
    # Create start menu entry (Windows)
    print("\n3. Installation complete!")
    print("\nYou can now:")
    print("• Double-click the desktop shortcut")
    print("• Run 'python sinhala_tts_app.py' from this folder")
    print("• Use the run_sinhala_tts.bat file")
    
    print("\n" + "=" * 60)
    print("Enjoy using the Sinhala TTS System!")
    print("=" * 60)

if __name__ == "__main__":
    main() 