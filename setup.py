"""
Setup script for Sinhala TTS Application
Run this script to install required dependencies
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3==2.98"])
        print("✓ pyttsx3 installed successfully")
        
        # Check if tkinter is available (it should be included with Python)
        try:
            import tkinter
            print("✓ tkinter is available (included with Python)")
        except ImportError:
            print("⚠ Warning: tkinter not found.")
            print("  On Linux: sudo apt-get install python3-tk")
            print("  On Windows: tkinter should be included with Python")
            print("  Try reinstalling Python from python.org")
            
        print("\nAll dependencies installed successfully!")
        print("You can now run the application with: python sinhala_tts_app.py")
        
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    return True

def check_system_requirements():
    """Check system requirements"""
    print("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check operating system
    if os.name == 'nt':
        print("✓ Windows OS detected")
    else:
        print("⚠ Warning: This application is optimized for Windows")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Sinhala TTS Application Setup")
    print("=" * 50)
    
    if check_system_requirements():
        if install_requirements():
            print("\n" + "=" * 50)
            print("Setup completed successfully!")
            print("Run 'python sinhala_tts_app.py' to start the application")
            print("=" * 50)
        else:
            print("\n❌ Setup failed!")
    else:
        print("\n❌ System requirements not met!") 