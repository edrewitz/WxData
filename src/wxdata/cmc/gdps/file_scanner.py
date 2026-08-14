"""
This file hosts the tools to scan the directories locally on the PC to ensure files are up to date.

(C) Eric J. Drewitz 2025-2026
"""
import os
from wxdata.cmc.utils.filenames import get_filenames

def scan_local_machine(urls,
                       path):
    
    """
    
    """
    
    download = False
    local_files = []
    if os.path.exists(f"{path}"):
        files = []
        for file in os.listdir(f"{path}"):
            files.append(file)
        try:    
            fname = files[-1]
            local_files.append(fname)
        except Exception as e:
            download = True
    
    else:
        download = True
        
    server_files = get_filenames(urls)

    try:
        if server_files[-1] == local_files[-1]:
            download = False
        else:
            local_file = local_files[-1]
            server_file = server_files[-1]
            local_file_date = local_file[0:10]
            server_file_date = server_file[0:10]
            if local_file_date == server_file_date:
                download = False
            else:
                download = True
    except Exception as e:
        download = True
        
    return download
    
    
        