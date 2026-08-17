"""
This file has the function that extracts filenames from the URL

(C) Eric J. Drewitz 2025-2026
"""
import os

from urllib.parse import urlparse

def get_filenames(urls):
    
    """
    Extracts filenames from URLs
    
    Required Arguments:
    
    1) urls (String List) - URLs for the download.
    
    Optional Arguments: None
    
    Returns
    -------
    
    Filenames from the URLs.
    """
    
    filenames = []
    
    for url in urls:
        path = urlparse(url).path
        file = os.path.basename(path)
        filenames.append(file)
        
    return filenames

