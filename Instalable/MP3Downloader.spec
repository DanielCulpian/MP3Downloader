# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MP3DownloaderV3.py'],
    pathex=[],
    binaries=[('bin/spotdl.exe', 'bin'), ('bin/ffmpeg/ffmpeg.exe', 'bin/ffmpeg'), ('bin/ffmpeg/ffprobe.exe', 'bin/ffmeg')],
    datas=[('bin/media/MP3Downloader.ico', 'bin/media')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='MP3Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bin/media/MP3Downloader.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MP3Downloader',
)
