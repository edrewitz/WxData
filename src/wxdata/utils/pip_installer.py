"""
This file hosts a function that automatically installs optional package dependencies.

(C) Eric J. Drewitz 2025-2026
"""

import subprocess
import sys

def installer(pkg_name):
    """
    Install a Python package at runtime using pip.
    Installs into the SAME environment running this script.
    
    Required Arguments: 
    
    1) pkg_name (String) - The package name. 
    
    Optional Arguments: None
    """

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", pkg_name
    ])

