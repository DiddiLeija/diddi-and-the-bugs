"""
Script to generate the Windows-only executable
(packaged as "windows.zip"). It uses cx_Freeze,
and generates everything by running the command
"setup.py build".

The reference for cx_Freeze can be found at
<https://github.com/marcelotduarte/cx_Freeze>.

After generating everything, get sure to add the
"resource.pyxres" at the "build/exe.{whatever that goes here}"
directory!
"""

import sys

try:
    from cx_Freeze import setup, Executable
except ImportError:
    sys.exit("COuld not find package 'cx_Freeze'. Please install it and try again.")

EXPECTED_PYTHON = (3, 7)
GAME_VERSION = "1.2.0"

if sys.platform != "win32":
    sys.exit(
        f"Error: Expected platform 'win32' for running this script, but got {sys.platform}"
    )
elif EXPECTED_PYTHON < sys.version_info:
    sys.exit(f"Error: Expected Python >= {EXPECTED_PYTHON}, but got {sys.version_info}")


setup(
    name="Diddi and the Bugs",
    version=GAME_VERSION,
    description="Diddi vs. Bugs!",
    author="Diego Ramirez",
    author_email="dr01191115@gmail.com",
    executables=[Executable("main.py", base="Win32GUI", )],
)
