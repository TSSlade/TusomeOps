# -*- mode: python -*-

block_cipher = None


a = Analysis(['mpesa_reformatter_no_pd.py'],
             pathex=['C:\\Dropbox\\Berkeley MIDS\\MIDS+\\Tusome\\TusomeOps\\Mpesa reformatter\\no_pd'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mpesa_reformatter_no_pd',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
