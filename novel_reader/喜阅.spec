# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\86139\\aipywork\\CapEwGvvipaKTj79zEPUj\\novel_reader\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('book_icon.ico', '.')],
    hiddenimports=['fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='喜阅',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\86139\\aipywork\\CapEwGvvipaKTj79zEPUj\\novel_reader\\book_icon.ico'],
)
