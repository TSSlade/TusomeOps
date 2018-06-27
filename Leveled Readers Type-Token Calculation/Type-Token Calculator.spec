# -*- mode: python -*-

block_cipher = None


a = Analysis(['Type-Token Calculator.py'],
             pathex=['C:\\Dropbox\\TSlade Stata\\Kenya Tusome\\gitrepos\\non-STATA\\Leveled Readers Type-Token Calculation'],
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
          name='Type-Token Calculator',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
