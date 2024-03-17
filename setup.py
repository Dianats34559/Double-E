import sys
from cx_Freeze import setup, Executable

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [Executable('main.py', base=base)]

includes = ['numpy', 'pandas', 'PIL', 'PyQt5',
            'pytz', 'screeninfo',
            'six', 'tzdata']

excludes = []

zip_include_packages = []


include_files = ['Data']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
    }
}

setup(name='Double-E',
      version='1.0',
      description='Clever Production: Double-E',
      executables=executables,
      options=options)
