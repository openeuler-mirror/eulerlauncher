# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../eulerlauncher/install.py'],
    pathex=[],
    binaries=[('../dist/eulerlauncher', './etc')],
    datas=[('../etc/eulerlauncher.conf', './etc'), ('../resources/qemu/edk2-aarch64-code.fd', './etc'), ('../resources/qemu/edk2-x86_64-code.fd', './etc')],
    hiddenimports=[],
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
    name='install',
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
)
