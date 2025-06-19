# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Collect data files for various packages
datas = []

# Add phoneme audio files
datas += [('phonemes', 'phonemes')]

# Add any additional data files if they exist
if os.path.exists('fonts'):
    datas += [('fonts', 'fonts')]

block_cipher = None

a = Analysis(
    ['enhanced_sinhala_tts.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pygame', 'tkinter', 'wave', 'json', 'threading', 'tempfile'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SinhalaTTS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
) 