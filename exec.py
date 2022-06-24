import sys
from cx_Freeze import setup, Executable

build_exe_options = {'packages':['os'], 'includes':['tkinter','turtle','config', 'interface','hashlib'], 'include_files':['images/','config/']}
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

# Cria o executável
setup(
    name="LockWeb",
    version="1.2",
    description="LockWeb v1.2",
    options={"build_exe":build_exe_options},
    executables=[Executable("Lockweb.py", base=base)]
)