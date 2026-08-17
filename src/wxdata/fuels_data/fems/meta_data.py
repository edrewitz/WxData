"""
This file hosts the functions that download and extract the meta-data for the various RAWS stations.

1) get_single_raws_station_meta_data
2) get_multi_raws_station_meta_data

(C) Eric J. Drewitz 2025-2026
"""
import pandas as _pd
import os as _os
import wxdata.client.client as _client
import numpy as _np

folder = _os.getcwd()
folder_modified = folder.replace("\\", "/") 

def get_single_raws_station_meta_data(station_id, 
                                        sheet_name='Sheet1',
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        proxies=None):
    
    """
    This function returns the meta-data for a specific user-defined RAWS station.
    
    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:

    1) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame. 
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the RAWS station meta-data.   
    """
    
    fname = f"RAWS Meta Data.xlsx"
    
    df = _client.get_excel_data(f"https://wildfireweb-prod-media-bucket.s3.us-gov-west-1.amazonaws.com/s3fs-public/2025-07/FEMS_3.0_RAWS_Master_Station_List_and_Metadata.xlsx",
                            path,
                            fname,
                            sheet_name,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
    
    
    keys = df.columns.tolist()
    
    row = (_np.where(df[keys[1]] == station_id))
    
    df = df.iloc[row]
    
    return df

def get_multi_raws_station_meta_data(station_ids, 
                                        sheet_name='Sheet1',
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        proxies=None):
    
    """
    This function returns the meta-data for a specific user-defined RAWS station.
    
    Required Arguments:

    1) station_ids (Integer List) - A list of RAWS Station IDs. 

    Optional Arguments:
    
    1) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame. 
    
    2) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    3) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. The directory the data will be saved to. 
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    A Pandas DataFrame of the RAWS station meta-data.   
    """
    
    fname = f"RAWS Meta Data.xlsx"
    
    df = _client.get_excel_data(f"https://wildfireweb-prod-media-bucket.s3.us-gov-west-1.amazonaws.com/s3fs-public/2025-07/FEMS_3.0_RAWS_Master_Station_List_and_Metadata.xlsx",
                            path,
                            fname,
                            sheet_name,
                            proxies=proxies,
                            notifications='off',
                            clear_recycle_bin=clear_recycle_bin)
    
    
    keys = df.columns.tolist()
    
    df_list = []
    
    for station_id in station_ids:
        row = (_np.where(df[keys[1]] == station_id))
    
        df_list.append(df.iloc[row])
        
    df = _pd.concat(df_list, ignore_index=True)
    
    return df