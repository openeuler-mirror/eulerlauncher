# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['omnivirt/macos-gui.py'],
    pathex=[],
    binaries=[('dist/OmniVirtd', './bin')],
    datas=[('etc/omnivirt.conf', './etc'), ('etc/images/favicon.png', './etc'), ('resources/qemu/edk2-aarch64-code.fd', './etc'), ('resources/qemu/edk2-x86_64-code.fd', './etc')],
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
    name='OmniVirt',
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
    uac_admin=True,
    icon=['etc/images/favicon.ico'],
)
app = BUNDLE(
    exe,
    name='OmniVirt.app',
    icon='etc/images/favicon.ico',
    bundle_identifier=None,
)
