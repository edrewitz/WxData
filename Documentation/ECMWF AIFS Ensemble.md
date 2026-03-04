# ECMWF AIFS Ensemble

***ecmwf_aifs_ens(final_forecast_hour=360,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    convert_temperature=True,
                    convert_to='celsius',
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    level_type='surface',
                    cat='control',
                    clear_data=False,
                    variables=['geopotential',
                                'total column water',
                                'mean sea level pressure',
                                'standard deviation of sub-gridscale orography',
                                'slope of sub-gridscale orography',
                                '10-meter u-wind component',
                                '10-meter v-wind component',
                                '2-meter temperature',
                                '2-meter dew point',
                                'surface shortwave radiation downward',
                                'land sea mask',
                                'surface longwave radiation downward',
                                'low cloud cover',
                                'mid-level cloud cover',
                                'high cloud cover',
                                'runoff water equivalent',
                                'convective precipitation',
                                'snowfall water equivalent',
                                'total cloud cover',
                                'total precipitation',
                                '100-meter u-wind component',
                                '100-meter v-wind component',
                                'skin temperature',
                                'surface pressure',
                                'specific humidity',
                                'relative humidity',
                                'temperature',
                                'u-wind component',
                                'v-wind component',
                                'vertical velocity',
                                'volumetric soil moisture content',
                                'soil temperature'],
                    levels=[1000, 
                            925, 
                            850, 
                            700, 
                            600, 
                            500, 
                            400, 
                            300, 
                            250, 
                            200, 
                            150, 
                            100, 
                            50],
                    members=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50]):***

    This function scans for the latest ECMWF IFS dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 360. The final forecast hour the user wishes to download. The ECMWF IFS
    goes out to 360 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    360 by the nereast increment of 3 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                           'http':'http://url',
                           'https':'https://url'
                        } 
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF AIFS Ensemble files will be saved to. 
        When set to None, the path will be: "ECMWF/AIFS/ENSEMBLE {cat}/"
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) level_type (String) - Default='surface'. The level of the parameters being queried. 
    
        level_types
        -----------
        
        1) 'surface'
        2) 'pressure'
        3) 'soil
    
    17) cat (String) - Default='control'. The type of ensemble run. 
    
        Control Run - cat='control'
        
        Ensemble Members - cat='members'
    
    18) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    19) variables (String List) - Default is all variables. The list of variable names in plain-language. 
    
        variables
        ---------
        
        'geopotential'
        'total column water'
        'mean sea level pressure'
        'standard deviation of sub-gridscale orography'
        'slope of sub-gridscale orography'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '2-meter temperature'
        '2-meter dew point'
        'surface shortwave radiation downward'
        'land sea mask'
        'surface longwave radiation downward'
        'low cloud cover'
        'mid-level cloud cover'
        'high cloud cover'
        'runoff water equivalent'
        'convective precipitation'
        'snowfall water equivalent'
        'total cloud cover'
        'total precipitation'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'skin temperature'
        'surface pressure'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'volumetric soil moisture content'
        'soil temperature'
        
    20) levels (Integer List) - Default=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]. 
        When level_type='pressure', this is the list of the pressure levels. 
        
        Example: User wants only the 500 mb level: levels=[500]
        
    21) members (Integer List) - Default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                          11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                          21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                          31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                          41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
                                          
        The ECMWF IFS Ensemble consists of 50 members. 
        
        Example: User wants only the first 5 members: members=[1,2,3,4,5]
        
    Returns
    -------
    
    An xarray data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF AIFS Ensemble Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'volumetric_soil_moisture_content'
    'soil_temperature'
    'geopotential'
    'specific_humidity'
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'vertical velocity'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'water_runoff' 
    'surface_geopotential_height'
    'skin_temperature'
    'surface_pressure'
    'standard_deviation_of_sub_gridscale_orography'
    'slope_of_sub_gridscale_orography'
    'surface_shortwave_radiation_downward'
    'land_sea_mask'
    'surface_longwave_radiation_downward'
    'convective_precipitation'
    'snowfall_water_equivalent'
    'total_precipitation'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'total_column_water'
    'total_cloud_cover'
    'mslp'
