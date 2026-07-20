"""
This file hosts the function that checks for the eccodes C++ library and returns a warning to the user if it is missing.

This is necessary as the eccodes C++ library is not compiled for the latest versions of Python

(C) Eric J. Drewitz 2025-2026
"""

import importlib.util as _import_util
import sys as _sys

VERSION = _sys.version_info

def _eccodes_warning_text():
    
    """
    Returns warning to the user if eccodes is not found
    """
    
    print(f"Warning: eccodes library is not compatible with Python {VERSION}.")
    print(f"For users who plan on working with GRIB files - Recommend switching to Python <= 3.13 as eccodes is compatible with Python <= 3.13")

def eccodes_warning():
    """
    Returns a warning if the eccodes C++ library is not found. 
    
    This is a common issue in newer versions of Python. 
    """
    package_name = "eccodes"
    package_exists = _import_util.find_spec(package_name) is not None

    if package_exists:
        pass
    else:
        _eccodes_warning_text()
        
        
def version_warning():
    
    """
    Warning for versions of Python not compatible with eccodes.
    """
    
    print("If the data has downloaded and the client tried re-downloading the data the issue is not likely due to connection issues.")
    print(f"The issue is most likely due to the version of eccodes not being compiled for Python == {VERSION}")