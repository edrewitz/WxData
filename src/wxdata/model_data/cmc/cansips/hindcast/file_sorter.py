"""
This file hosts the file sorter for the CanSIPS Hindcast Files.

(C) Eric J. Drewitz 2025-2026
"""

import os
import shutil

from urllib.parse import urlparse


def create_directories(path,
                       variable):
    
    """
    Creates file directories for each year.
    
    Required Arguments:
    
    1) path (String) - The path of the base directory.
    
    2) variable (String) - The variable requested by the user. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A series of directories binned by year.
    """
    
    for i in range(1991, 2021, 1):
        os.makedirs(f"{path}/{i}/{variable.upper()}", 
                    exist_ok=True)
        

def sort_files(path,
               urls,
               variable):
    
    """
    Sorts the files into their proper bins from the temporary folder
    
    Required Arguments:
    
    1) path (String) - The path of the base directory.
    
    2) urls (String List) - List of URLs to extract the filenames.
    
    3) variable (String) - The variable requested by the user. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    Moves the files from the temporary folder into their respective folders.
    """
    
    create_directories(path,
                       variable)
    
    files = []
    for url in urls:
        parsed_url = urlparse(url)
        basename = os.path.basename(parsed_url.path)
        files.append(basename)
        
    # Extract sorted unique years
    years = sorted({int(f[:4]) for f in files})

    # Build bins as a list of lists
    bins = [
        [f for f in files if int(f[:4]) == year]
        for year in years
    ]
    
    for year, bin in zip(years, bins):
        for file in bin:
            try:
                os.replace(f"{path}/Temp/{file}", f"{path}/{year}/{variable.upper()}/{file}")
            except Exception as e:
                pass
            
    try:
        shutil.rmtree(f"{path}/Temp")
    except Exception as e:
        pass

        