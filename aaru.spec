# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for building AARU CLI executable
Usage: pyinstaller aaru.spec
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all aarush package data
datas = []
datas += collect_data_files('aarush')

# Add ASCII art file
ascii_art_path = os.path.join('aarush', 'ascii-profile', 'ascii-art.txt')
if os.path.exists(ascii_art_path):
    datas.append((ascii_art_path, 'aarush/ascii-profile'))

# Collect all submodules
hiddenimports = []
hiddenimports += collect_submodules('aarush')
hiddenimports += collect_submodules('typer')
hiddenimports += collect_submodules('click')

a = Analysis(
    ['aarush/aaru_cli.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='aaru',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon='icon.ico' if you have an icon file
)
