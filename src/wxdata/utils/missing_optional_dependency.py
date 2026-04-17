"""
This file hosts a function that warns a user that is missing an optional dependency.

(C) Eric J. Drewitz 2025-2026
"""

import os
import sys

def install_method(pkg_name):
    
    """
    This function checks to see if an existing package is installed via anaconda or pip
    
    Required Arguments:
    
    1) pkg_name (String) - The name of the package.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A boolean value determining if the package is installed via pip (False) or anaconda (True). 
    """
    
    conda_meta = os.path.join(sys.prefix, "conda-meta")
    if not os.path.isdir(conda_meta):
        return False  # not a conda env at all
    for fn in os.listdir(conda_meta):
        if fn.startswith(pkg_name.replace("-", "_")) and fn.endswith(".json"):
            return True
    return False


def optional_dependency_not_found(pkg_name):
    
    """
    This function prints a message to the user instructing them how to resolve the missing dependency.
    
    Required Arguments: 
    
    1) pkg_name (String) - The name of the package.
    
    Return
    ------
    
    A message to the user instructing them that pkg_name is missing and instructions how to resolve.    
    """
    
    conda = install_method(pkg_name)
    
    if conda == True:
        method = 'conda'
    else:
        method = 'pip'
        
    print(f"User is missing optional dependency: {pkg_name}")
    print(f"Resolve this by running: {method} install {pkg_name}")
    
    