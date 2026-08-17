"""
This file hosts the tools to scan the directories locally on the PC to ensure files are up to date.

(C) Eric J. Drewitz 2025-2026
"""
import os
from wxdata.model_data.cmc.utils.filenames import get_filenames

def scan_local_machine(urls,
                       path):
    
    """
    This function scans the files on the local machine and compares the filenames on the local
    machine to the files scanned on the https://dd.weather.gc.ca/ via the url scanner. 
    
    If the dates in the filenames on the local machine match those on the server, a value of 
    download=False is returned and the download is bypassed by the client to prevent an 
    HTTP 429 (too many requests) response. 
    
    If the dates in the filenames on the local machine do not match with those on the server, a value of
    download=True is returned to tell the client it is time to clear out the directory and download the new data.
    
    A value of download=True is also returned for first time downloads or users who change their path the first time
    they run the client. 
    
    Returns
    -------
    
    downloads - A boolean value that tells the client to initiate a download for the new data on the https://dd.weather.gc.ca/ server.
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
    
    
        