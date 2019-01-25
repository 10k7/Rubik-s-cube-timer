"""This is a complier program. It converts the python file "CubeTimer.py" into a windows executable file."""


from cx_Freeze import setup, Executable
import sys
import os
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform == "win32":
    base = "Win32GUI"


syspath = r"C:\Users\jerea\AppData\Local\Programs\Python\Python37/DLLS"


setup(
    name = "CubeTimer",
    version = '0.1',
    description = 'Rubiks cube timer',
    options = {'build_exe': {'packages': ['tkinter'],
                'include_files': ['2x2.gif', '3x3.gif', '4x4.gif', 'x.gif', syspath + '/tcl86t.dll', syspath + '/tk86t.dll']}},
    executables = [Executable('CubeTimer.py', base=base, icon="cube_icon_Ue5_icon.ico")],
)