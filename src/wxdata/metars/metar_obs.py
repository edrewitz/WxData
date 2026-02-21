"""
This module has the functions that download, unzip and return METAR data. 

(C) Eric J. Drewitz 2025-2026
"""

import pandas as _pd 
import csv as _csv
import urllib.request as _request
import os as _os
import time as _time
import wxdata.metars._clean_data as _clean_data

from wxdata.calc.kinematics import get_u_and_v as _get_u_and_v
from wxdata.calc.thermodynamics import relative_humidity as _relative_humidity
from wxdata.utils.file_funcs import extract_gzipped_file as _extract_gzipped_file
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

def _get_csv_column_names_csv_module(file_path):
    """
    This function extracts the header in a CSV file. 
    
    Required Arguments:
    
    1) file_path (String) - The path to the file.
    
    Optional Arguments: None
    
    Returns
    -------
    
    The headers of the contents in the CSV file. 
    """
    with open(file_path, 'r', newline='') as csvfile:
        reader = _csv.reader(csvfile)
        header = next(reader) 
        return header

def download_metar_data(clear_recycle_bin=False):
    
    """
    Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        

    Returns:        
    pd.DataFrame: A DataFrame containing the METAR data.
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _request.urlretrieve(f"https://aviationweather.gov/data/cache/metars.cache.csv.gz", f"metars.cache.csv.gz")
    except Exception as e:
        for i in range(0, 6, 1):
            _time.sleep(30)
            try:
                _request.urlretrieve(f"https://aviationweather.gov/data/cache/metars.cache.csv.gz", f"metars.cache.csv.gz")
                break
            except Exception as e:
                i = i
    _extract_gzipped_file('metars.cache.csv.gz', 'metars.csv')
    
    if _os.path.exists(f"METAR Data"):
        pass
    else:
        _os.mkdir(f"METAR Data")

    try:
        for file in _os.listdir(f"METAR Data"):
            _os.remove(f"METAR Data/{file}")
    except Exception as e:
        pass
        
    _os.replace(f"metars.csv", f"METAR Data/metars.csv")

    with open('METAR Data/metars.csv', 'r', newline='') as csvfile:
        # Create a reader object
        csv_reader = _csv.reader(csvfile)
        rows = []
        for row in csv_reader:
            rows.append(row)
    
    data = []
    for i in range(0, len(rows), 1):
        if i > 4:
            data.append(rows[i])
            
    df = _pd.DataFrame(data)
    
    new_column_names = _get_csv_column_names_csv_module(f"METAR Data/metars.csv")
    
    df.columns = new_column_names

    df = df.drop('raw_text', axis=1)

    df = df.drop(index=0)
    
    df = _clean_data.clean_data(df)
    
    df['u_wind'], df['v_wind'] = _get_u_and_v(df['wind_speed'], df['wind_direction'])
    df['relative_humidity'] = _relative_humidity(df['temperature'], df['dew_point'])
    
    return df