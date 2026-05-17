"""
This file hosts the exception messages that could happen across a good portion of the package.

(C) Eric J. Drewitz 2025-2026
"""

import sys
import importlib.util


VERSION = sys.version_info

VERSION = f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"

def eccodes_error_message_text():
    
    print(f"eccodes package was unable to be properly installed in this environment.")
    
    print(f"Python Version: {VERSION}")
    
    print(f"This error is likely due to the version of eccodes needed in this environment is not compiled on pypi")
    
    print(f"To fix this issue there are two options you can do:")
    
    print(f"Option 1: Create a new Python environment and use Anaconda/Miniconda3 to install: conda install wxdata")
    
    print(f"Option 2: Create a new Python environment with a Python Version < {VERSION} and install via pip: pip install wxdata")
    
    
    
def eccodes_error_message():
    
    """
    This function checks for the installation of eccodes.
    
    eccodes is a C++ library developed by ECMWF and is a required dependency of xarray to process GRIB data.
    
    Later versions of Python have issues with eccodes installation if the user is using pip over miniconda3.
    
    Returns
    -------
    
    If eccodes is not installed, an error message is returned to the user.     
    """
    
    package_name = 'eccodes'
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        pass
    else:
        eccodes_error_message_text()
        sys.exit(1)