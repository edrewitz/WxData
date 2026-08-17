"""
This file hosts the local file scanner for CFS files.

(C) Eric J. Drewitz 2025-2026
"""
import os

def cfs_file_scanner(path,
                     files):
    
    """
    This function scans to compare the final forecast file in the local directory with the latest available final forecast
    file on the NOMADS Server.
    
    If the files match, a boolean value of False will be returned.
    If the files do not match, a boolean value of True will be returned.
    
    Required Arguments:
    
    1) path (String) - The path to the files in the local directory.
    
    2) files (String List) - The list of files returned from the URL scanner.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A value of True or False to initiate downloading new files.    
    """
    
    try:
        file_list = []
        for file in os.listdir(f"{path}"):
            file_list.append(file)
        
        if files[-1] == file_list[-1]:
            download = False
        else:
            download = True
    except Exception as e:
        download = True
        
    return download