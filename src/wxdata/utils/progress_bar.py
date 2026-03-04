"""
This file hosts a function that displays a progress bar for downloading a file.

(C) Eric J. Drewitz 2025-2026
"""


import os

from tqdm import tqdm

def progress_bar(response,
                 path,
                 filename,
                 blocksize=1024):
    
    """
    This function creates a progress bar for downloading each file in the client.
    
    Required Arguments:
    
    1) response (HTTP Response) - The server response.
    
    2) path (String) - The path to the file. 
    
    3) filename (String) - The name of the file. 
    
    Optional Arguments:
    
    1) blocksize (Integer) - Default=1024 (1KB)
    
    Returns
    -------
    
    A progress bar for downloading a file.     
    """
    
    total_size = int(response.headers.get("content-length", 0))
    
    with tqdm(total=total_size, unit="B", unit_scale=True, desc=filename, leave=False, colour='black', miniters=1) as bar:
        with open(f"{path}/{filename}", "wb") as file:
            for data in response.iter_content(blocksize):
                file.write(data)
                bar.update(len(data))