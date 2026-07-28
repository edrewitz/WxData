# FEMS: Single RAWS Station Meta-Data

***def get_single_raws_station_meta_data(station_id, 
                                        sheet_name='Sheet1',
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        proxies=None):***


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
