# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../eulerlauncher/macos-gui.py'],
    pathex=[],
    binaries=[('../dist/eulerLauncherd', './bin')],
    datas=[('../etc/eulerlauncher.conf', './etc'), ('../etc/images/favicon.png', './etc'), ('../resources/libvirt/libvirt-aarch64.xml', './etc')],
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
    name='EulerLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['etc/images/favicon.ico'],
)

app = BUNDLE(
    exe,
    name='EulerLauncher.app',
    icon='../etc/images/favicon.ico',
    bundle_identifier=None,
)
