"""
This file hosts the exception messages that could happen across a good portion of the package.

(C) Eric J. Drewitz 2025-2026
"""

import sys

VERSION = sys.version_info

VERSION = f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"

def eccodes_error_message():
    
    print(f"eccodes package was unable to be properly installed in this environment.")
    
    print(f"Python Version: {VERSION}")
    
    print(f"This error is likely due to the version of eccodes needed in this environment is not compiled on pypi")
    
    print(f"To fix this issue there are two options you can do:")
    
    print(f"Option 1: Create a new Python environment and use Anaconda/Miniconda3 to install: conda install wxdata")
    
    print(f"Option 2: Create a new Python environment with a Python Version < {VERSION} and install via pip: pip install wxdata")