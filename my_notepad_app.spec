# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Pro-Multi-Tab-Notepad.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'customtkinter',
        'markdown2',
        'pypandoc',
        'requests',
        'packaging',
        'config',
        'ui_components',
        'mixins',
        'mixins.tab_operations',
        'mixins.file_operations',
        'mixins.search_operations',
        'mixins.settings_operations',
        'mixins.markdown_operations',
        'mixins.import_operations',
    ],
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
    name='my_notepad_app',
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
    icon='icon\\icon-win.ico',
)
