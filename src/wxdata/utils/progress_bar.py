"""
This file hosts a function that displays a progress bar for downloading a file.

(C) Eric J. Drewitz 2025-2026
"""

import sys

def is_jupyter_notebook() -> bool:
    """
    Checks if the code is running within a Jupyter Notebook environment.
    
    Returns:
    --------
    bool
        True if running in a Jupyter Notebook/Lab, False otherwise.
    """
    # 1. Quick check for the ipykernel module in active memory
    if 'ipykernel' not in sys.modules:
        return False
        
    # 2. Confirm by checking the active IPython shell type
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except (ImportError, NameError):
        return False   # Probably standard Python interpreter
    
NOTEBOOK = is_jupyter_notebook()

if NOTEBOOK == False:
    from tqdm.auto import tqdm
else:
    from tqdm.notebook import tqdm

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
