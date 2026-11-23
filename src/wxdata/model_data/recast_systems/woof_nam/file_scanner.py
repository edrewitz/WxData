"""
Scans the local directory to check to see if the local files are up to date with the latest files on the server.

(C) Eric J. Drewitz 2025-2026
"""

import os
import time

from datetime import datetime
    
# Gets local time
local = datetime.now()

def local_file_scanner(path,
                       run,
                       filename):
    
    """
    Scans the local directory to check to see if the local files are up to date with the latest files on the server.
    
    Required Arguments:
    
    1) path (String) - The path of the directory.
    
    2) run (Integer) - The model runtime from the URL scanner.'
    
    3) filename (String) - The filename of the file with the latest data.
    
    Optional Arguments: None
    
    **Returns**
    
    A boolean value of True if there is a mismatch and False if everything matches    
    """
    
    download = True
    
    if os.path.exists(f"{path}/{filename}"):
        mrun = int(filename[10:12])
        if run == mrun:
            modification_timestamp = os.path.getmtime(f"{path}/{filename}")
            readable_time = time.ctime(modification_timestamp)
            update_day = int(f"{readable_time[8]}{readable_time[9]}")
            if update_day != local.day:
                pass
            else:
                download = False
        else:
            pass
    else:
        pass
    
    return download
            
