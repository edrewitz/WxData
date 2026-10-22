"""
This file hosts the validation for the ECMWF files to ensure user has the correct `level_type`

(C) Eric J. Drewitz 2025-2026
"""

import os
import sys

def validate_file(path,
                  filename):
    
    """
    Validates the file to ensure it is not 0 bytes. 
    
    If the file is 0 bytes an error message will be returned to the user.
    
    Required Arguments:
    
    1) path (String) - The directory the file is in.
    
    2) filename (String) - The name of the file.
    
    Returns
    -------
    
    An error message if the file is 0 bytes.    
    """
    
    size = os.path.getsize(f"{path}/{filename}")
    
    if size > 0:
        pass
    else:
        print(f"Error: File size is 0 Bytes.")
        print(f"This is likely attributed to an incorrect `level_type` for the requested `variables`.")
        print(f"Double check to make sure your `level_type` reflects the `variables`.")
        print(f"Example: if variables=['geopotential height'] -> level_type='pressure'.")
        print("System Exit...")
        sys.exit(1)