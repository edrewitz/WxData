"""
This utility verifies the file size of GRIB2 files to retry downloading corrupted files.

(C) Eric J. Drewitz 2025-2026
"""

import os

def verify_file(path,
                filename):
    
    """
    Verifies and returns filesize for each file.
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    2) filename (String) - Filename.
    
    Optional Arguments: None
    
    Returns
    -------
    
    verify - Returns True if the file size > 1KB and False if filesize <= 1KB.     
    """
    
    size = os.path.getsize(f"{path}/{filename}")
    
    size = size * 0.001
    
    if size <= 1:
        verify = False
    else:
        verify = True
    
    return verify