# Sinhala TTS - Windows Installer Creation Guide

This guide will help you create a professional Windows installer for your Sinhala Text-to-Speech application.

## Prerequisites

### 1. Install Required Software

**Inno Setup (Required for installer creation):**

- Download from: https://jrsoftware.org/isdl.php
- Install the latest version (6.x recommended)
- Choose default installation options

**Python Environment:**

- Ensure Python 3.7+ is installed
- Virtual environment with required packages

### 2. Prepare Your Project

Ensure your project structure looks like this:

```
assignment/
├── enhanced_sinhala_tts.py        # Main application
├── sinhala_text_to_phoneme.py     # Phoneme converter
├── phonemes/                      # Audio files directory
│   ├── a.wav
│   ├── aa.wav
│   └── ... (all phoneme files)
├── env/                          # Virtual environment
├── requirements.txt              # Dependencies
├── sinhala_tts.spec             # PyInstaller spec
├── installer.iss                # Inno Setup script
├── create_installer.bat         # Build script
├── README.md                    # Documentation
└── LICENSE.txt                  # License file
```

## Quick Start (Automated)

### Method 1: One-Click Build

1. **Open Command Prompt as Administrator**
2. **Navigate to your project directory:**
   ```cmd
   cd "D:\L4S2\NLP\assignment"
   ```
3. **Run the build script:**
   ```cmd
   create_installer.bat
   ```

The script will:

- Check all required files
- Install PyInstaller
- Build the executable
- Create the Windows installer
- Place the final installer in `installer_output/`

## Manual Steps (Advanced)

### Step 1: Build the Executable

```cmd
# Activate virtual environment
env\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller sinhala_tts.spec
```

### Step 2: Create the Installer

1. **Open Inno Setup**
2. **Open the script file:** `installer.iss`
3. **Click Build → Compile**
4. **Wait for compilation to complete**

The installer will be created in `installer_output/SinhalaTTS_Setup_v1.0.exe`

## Customization Options

### Modify Application Details

Edit `installer.iss` to customize:

```iss
#define MyAppName "Your App Name"
#define MyAppVersion "2.0"
#define MyAppPublisher "Your Company"
#define MyAppURL "https://your-website.com"
```

### Add Custom Icon

1. Create or obtain an `.ico` file
2. Save it as `icon.ico` in your project root
3. The build script will automatically include it

### Include Additional Files

Edit `installer.iss` to add more files:

```iss
[Files]
Source: "your-file.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs
```

## Troubleshooting

### Common Issues

**"PyInstaller not found"**

- Solution: Install with `pip install pyinstaller`
- Ensure virtual environment is activated

**"Inno Setup not found"**

- Solution: Install Inno Setup from official website
- Ensure it's installed in default location

**"phonemes directory not found"**

- Solution: Ensure phoneme audio files are in `phonemes/` folder
- Check that WAV files exist and are valid

**"Module not found" errors**

- Solution: Add missing modules to `hiddenimports` in `sinhala_tts.spec`
- Install missing packages with pip

**Large executable size**

- Solution: Use `--exclude-module` in PyInstaller for unused packages
- Consider using UPX compression (already enabled)

### Build Optimization

**Reduce file size:**

```python
# In sinhala_tts.spec, add to excludes:
excludes=['numpy', 'scipy', 'matplotlib', 'PIL', 'cv2']
```

**Include only required phonemes:**

```python
# Only include used phoneme files
datas += [('phonemes/essential', 'phonemes')]
```

## Testing the Installer

### Before Distribution

1. **Test on clean Windows system**
2. **Verify all features work:**

   - Text-to-speech functionality
   - Audio playback
   - File operations
   - Settings persistence

3. **Check installer behavior:**
   - Installation process
   - Desktop shortcut creation
   - Uninstallation process

### Compatibility Testing

Test on different Windows versions:

- Windows 10
- Windows 11
- Different architectures (if applicable)

## Distribution

### Digital Signing (Recommended)

For professional distribution:

1. Obtain a code signing certificate
2. Sign the installer with `signtool`
3. This prevents security warnings

### File Sharing

**Safe distribution methods:**

- Company website download
- GitHub releases
- Professional file hosting

**Include with installer:**

- README file
- System requirements
- Contact information

## Advanced Configuration

### Custom Installation Options

Add installation choices in `installer.iss`:

```iss
[Components]
Name: "main"; Description: "Main application"; Types: full compact custom; Flags: fixed
Name: "phonemes"; Description: "Complete phoneme library"; Types: full
Name: "samples"; Description: "Sample texts"; Types: full
```

### Registry Settings

Store application settings:

```iss
[Registry]
Root: HKCU; Subkey: "Software\YourCompany\SinhalaTTS"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
```

### Multiple Languages

Add language support:

```iss
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "sinhala"; MessagesFile: "compiler:Languages\Sinhala.isl"
```

## Version Management

### Updating the Application

1. **Update version number** in `installer.iss`
2. **Modify uninstall behavior** for upgrades
3. **Test upgrade scenarios**

### Automated Builds

Create CI/CD pipeline:

- Automatic building on code changes
- Version tagging
- Automated testing
- Release deployment

## Final Checklist

Before distributing your installer:

- [ ] Application runs correctly from installer
- [ ] All phoneme files included and working
- [ ] Desktop shortcut works
- [ ] Start menu entry created
- [ ] Uninstaller removes all files
- [ ] No registry remnants after uninstall
- [ ] Installer works on clean Windows system
- [ ] File associations work (if any)
- [ ] Documentation included and accessible

## Support and Updates

For questions or issues:

1. Check this guide first
2. Review PyInstaller documentation
3. Consult Inno Setup help
4. Test on different systems

Remember to keep backups of your working build configuration!
