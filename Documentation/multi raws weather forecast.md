# FEMS: Multi RAWS Station Weather Forecast

***def get_multi_raws_station_weather_forecast(station_ids, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Multi Station/Weather Forecasts',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):***

    This function retrieves the 7-Day weather forecast for a user-specified list of RAWS stations. 

    Required Arguments:

    1) station_ids (Integer List) - An integer list of all the RAWS IDs for each RAWS station the user wants in the dataset.

    Optional Arguments:
    
    1) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    2) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Forecasts'. 
        The directory the data will be saved to. 
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    4) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    5) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    6) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of 7-Day weather forecast data for a user-specified list of RAWS stations.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.          
