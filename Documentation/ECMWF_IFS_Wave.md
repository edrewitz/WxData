# ECMWF IFS Wave

***def ecmwf_ifs_wave(final_forecast_hour=144,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    step=3,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    clear_data=False,
                    variables=['mean zero-crossing wave period',
                                'mean wave direction',
                                'mean wave period',
                                'peak wave period']):***

    This function scans for the latest ECMWF IFS Wave dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 144.

        00z and 12z ECMWF IFS Wave Runs
        -------------------------------
        
        3-Hourly Increments from hour 0 to hour 144.
        6-Hourly Increments from hour 144 to hour 360
        
        06z and 18z ECMWF IFS Wave Runs
        -------------------------------
        
        3-Hourly Increments from hour 0 to hour 144.  
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port"
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = "ECMWF/IFS/WAVE"
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'.
        
    15) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
    
    16) variables (String List) - Default is all variables. The list of variable names in plain-language. 
    
        variables
        ---------
        
        'mean zero-crossing wave period'
        'mean wave direction'
        'mean wave period'
        'peak wave period'
        
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Wave Variable Keys (After Post-Processing)
    -------------------------------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'
