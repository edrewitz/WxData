# FEMS: Single RAWS Station Weather Observations

***def get_single_raws_station_weather_observations(station_id, 
                                        number_of_days=7, 
                                        start_date=None, 
                                        end_date=None, 
                                        clear_recycle_bin=False,
                                        path=f'{folder_modified}/FEMS Data/Single Station/Observations/Weather',
                                        proxies=None,
                                        clear_data=True,
                                        meta_path=f'{folder_modified}/FEMS Data/Station Meta Data',
                                        sheet_name='Sheet1'):***

    This function retrieves the observed weather data for a user-specified single RAWS station for a 
    user-specified period of time. 

    Required Arguments:

    1) station_id (Integer) - The RAWS ID of the station. 

    Optional Arguments:
    
    1) number_of_days (Integer or String) - Default=7. How many days the user wants the summary for (90 for 90 days).
        If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

    2) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-ddTH:M:S'

    3) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
        in the following format 'YYYY-mm-ddTH:M:S'
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be deleted 
        with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default=f'{folder_modified}/FEMS Data/Single Station/Observations/Weather'. 
        The directory the data will be saved to. 
        
    6) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    7) clear_data (Boolean) - Default=True. When set to True, the data directory clears out and new data is downloaded.
    
    8) meta_path (String) - Default=f'{folder_modified}/FEMS Data/Station Meta Data'. 
        The path to where the RAWS station meta data excel file will be saved to. 
        
    9) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame.
    
    Returns
    -------
    
    1) A Pandas DataFrame of observed weather data for a user-specified single RAWS station for a user-specified time.   
    2) A Pandas DataFrame of the RAWS Station Meta-Data.    
