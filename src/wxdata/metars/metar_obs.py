"""
This module has the functions that download, unzip and return METAR data. 

(C) Eric J. Drewitz 2025
"""

import pandas as pd
import csv
import wxdata.client.client as client

from wxdata.calc.kinematics import get_u_and_v
from wxdata.utils.file_funcs import extract_gzipped_file
from wxdata.utils.recycle_bin import *

def get_csv_column_names_csv_module(file_path):
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
        reader = csv.reader(csvfile)
        header = next(reader) 
        return header

def download_metar_data(clear_recycle_bin=False,
                        proxies=None,
                        notifications='off'):
    
    """
    Downloads the latest METAR Data from NOAA/AWC and returns a Pandas DataFrame.
    
    Required Arguments: None
    
    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
                        
    3) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

    Returns:        
    pd.DataFrame: A DataFrame containing the METAR data.
    """
    if clear_recycle_bin == True:
        clear_recycle_bin_windows()
        clear_trash_bin_mac()
        clear_trash_bin_linux()
    else:
        pass
    
    client.get_csv_data("https://aviationweather.gov/data/cache/metars.cache.csv.gz",
                        f"METAR Data",
                        f"metars.cache.csv.gz",
                        proxies=proxies,
                        notifications=notifications,
                        return_pandas_df=False,
                        clear_recycle_bin=clear_recycle_bin)
    
    extract_gzipped_file('METAR Data/metars.cache.csv.gz', 'METAR Data/metars.csv')

    with open('METAR Data/metars.csv', 'r', newline='') as csvfile:
        # Create a reader object
        csv_reader = csv.reader(csvfile)
        rows = []
        for row in csv_reader:
            rows.append(row)
    
    data = []
    for i in range(0, len(rows), 1):
        if i > 4:
            data.append(rows[i])
            
    df = pd.DataFrame(data)
    
    new_column_names = get_csv_column_names_csv_module(f"METAR Data/metars.csv")
    
    df.columns = new_column_names

    df = df.drop('raw_text', axis=1)

    df = df.drop(index=0)
    
    df['u_wind'], df['v_wind'] = get_u_and_v(df['wind_speed_kt'], df['wind_dir_degrees'])
    
    return df