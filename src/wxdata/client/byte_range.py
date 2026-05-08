"""
This file hosts the function that fetches the byte-range for a variable.

(C) Eric J. Drewitz 2025-2026
"""

import requests

from tqdm.auto import tqdm


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
                         stream=True)
    else:
        response = requests.get(url, 
                         headers=headers,
                         proxies=proxies,
                         stream=True)
    
    response.raise_for_status()
    response.close()
    
    if len(response.content) == 0:
        if proxies == None:
            response = requests.get(url, 
                            headers=headers)
        else:
            response = requests.get(url, 
                            headers=headers,
                            proxies=proxies)
    else:
        pass
    
    return response


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

            # Inner bar (disappears after finishing)
            with tqdm(
                    total=total_bytes,
                    unit="B",
                    unit_scale=True,
                    bar_format="{desc} {bar} {percentage:3.0f}%",
                    ncols=80,
                    leave=False
                ) as pbar:
                
                    pbar.set_description(f"{var} @ {level}")
                
                    for chunk in results.iter_content(chunk_size=chunk_size):
                        if chunk:
                            data += chunk
                            pbar.update(len(chunk))

            master.update(1)

    master.close()
