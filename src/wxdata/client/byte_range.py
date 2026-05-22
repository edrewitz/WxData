"""
This file hosts the function that fetches the byte-range for a variable.

(C) Eric J. Drewitz 2025-2026
"""

import requests

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


def fetch_range(url, 
                start, 
                end,
                proxies):
    
    """
    This function downloads the data corresponding to the bytes-range for each variable
    
    Required Arguments:
    
    1) url (String) - The URL of the GRIB file that will be downloaded.
    
    2) start (Integer) - The starting byte.
    
    3) end (Integer) - The ending byte.
    
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    The data to be written to a GRIB file.
    """
    
    headers = {"Range": f"bytes={start}-{end}" if end else f"bytes={start}-"}
    
    if proxies == None:
        response = requests.get(url, 
                         headers=headers,
                         allow_redirects=True,
                         stream=True)
    else:
        response = requests.get(url, 
                         headers=headers,
                         allow_redirects=True,
                         proxies=proxies,
                         stream=True)
    
    response.raise_for_status()
    response.close()
    
    if len(response.content) == 0:
        if proxies == None:
            response = requests.get(url,
                            allow_redirects=True, 
                            headers=headers)
        else:
            response = requests.get(url,
                            allow_redirects=True, 
                            headers=headers,
                            proxies=proxies)
    else:
        pass
    
    return response.content


def fetch_data(ranges,
                url, 
                start, 
                end,
                proxies):
    
    """
    This function downloads the data corresponding to the bytes-range for each variable
    
    Required Arguments:
    
    1) url (String) - The URL of the GRIB file that will be downloaded.
    
    2) start (Integer) - The starting byte.
    
    3) end (Integer) - The ending byte.
    
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    The data to be written to a GRIB file.
    """
    
    results = {}
    for (v, l), (start, end) in ranges.items():
        results[(v, l)] = fetch_range(
            url,
            start,
            end,
            proxies
        )

    return results


def download_grib_data_by_byte_range(ranges,
                             chunk_size,
                             path,
                             filename,
                             grib_url,
                             start,
                             end,
                             proxies):
    """
    results: dict[(var, level)] = bytes
    Writes all GRIB messages to a single file with polished progress bars.
    
    This function writes the GRIB file with a progress bar. 
    This is a progress bar for the byte-range requests. 
    
    Required Arguments:
    
    1) ranges (Tuple List) - A tuple list of byte-ranges.
    
    2) chunk_size (Integer) - The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) path (String) - The directory where the file is saved to. 
    
    4) filename (String) - The name the user wishes to save the file as. 
    
    5) grib_url (String) - The URL of the GRIB file that will be downloaded.
    
    6) start (Integer) - The starting byte.
    
    7) end (Integer) - The ending byte.
    
    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Optional Arguments: None
    
    Returns
    -------
    
    A GRIB file of {filename} saved to {path}
    """
    
    results = fetch_data(ranges,
                            grib_url, 
                            start, 
                            end,
                            proxies)

    ordered = sorted(results.items(), key=lambda x: (x[0][0], x[0][1]))

    # Master progress bar (stays visible)
    master = tqdm(
        total=len(ordered),
        desc="Writing GRIB messages",
        position=0,
        leave=False,
        bar_format="{desc:<25} |{bar:30}| {n}/{total}"
    )

    with open(f"{path}/{filename}", "wb") as f:
        for (var, level), data in ordered:

            total_bytes = len(data)
            label = f"{var} @ {level}"

            # Inner bar (disappears after finishing)
            with tqdm(
                total=total_bytes,
                unit="B",
                unit_scale=True,
                unit_divisor=chunk_size,
                desc=label,
                position=1,
                leave=False,
                bar_format="{desc:<30} |{bar:30}| {percentage:3.0f}% [{n_fmt}/{total_fmt}]"
            ) as pbar:

                for i in range(0, total_bytes, chunk_size):
                    chunk = data[i:i+chunk_size]
                    f.write(chunk)
                    pbar.update(len(chunk))

            master.update(1)

    master.close()