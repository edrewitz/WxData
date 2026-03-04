# ECMWF IFS Ensemble

***ecmwf_ifs_ens(final_forecast_hour=144,
              western_bound=-180,
              eastern_bound=180,
              northern_bound=90,
              southern_bound=-90,
              step=3,
              proxies=None,
              process_data=True,
              clear_recycle_bin=False,
              convert_temperature=True,
              convert_to='celsius',
              custom_directory=None,
              notifications='off',
              source='ecmwf',
              level_type='surface',
              clear_data=False,
              variables=['Geopotential (step 0)',
                        'Standard deviation of sub-gridscale orography (step 0)',
                        '10-meter u-wind component',
                        '10-meter v-wind component',
                        '100-meter u-wind component',
                        '100-meter v-wind component',
                        'maximum 10-meter wind gust step 0',
                        'maximum 10-meter wind gust steps 3-144',
                        '2-meter temperature',
                        '2-meter dewpoint temperature',
                        'mean sea level pressure',
                        'mean zero-crossing wave period',
                        'mean wave direction',
                        'mean wave period',
                        'peak wave period',
                        'significant wave height',
                        'runoff',
                        'total precipitation',
                        'surface pressure',
                        'total column vertically integrated water vapor',
                        'total cloud cover',
                        'snow depth water equivalent',
                        'snowfall water equivalent',
                        'land sea mask',
                        'volumetric soil moisture content',
                        'soil temperature',
                        'most unstable cape',
                        'snow albedo',
                        '3-hour minimum 2-meter temperature',
                        '3-hour maximum 2-meter temperature',
                        '6-hour minimum 2-meter temperature',
                        '6-hour maximum 2-meter temperature',
                        'total precipitation rate',
                        'precipitation type',
                        'top net longwave thermal radiation',
                        'snow density',
                        'surface net longwave thermal radiation',
                        'surface net shortwave solar radiation',
                        'surface shortwave radiation downward',
                        'surface longwave radiation downward',
                        'northward turbulent surface stress',
                        'eastward turbulent surface stress',
                        'eastward surface sea water velocity',
                        'northward surface sea water velocity',
                        'sea ice thickness',
                        'sea surface height',
                        'divergence',
                        'geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component',
                        'vertical velocity',
                        'relative vorticity'],
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

    This function scans for the latest ECMWF IFS Ensemble dataset. If the dataset on the computer is old, the old data will be deleted
    and the new data will be downloaded. 
    
    1) final_forecast_hour (Integer) - Default = 144.

        00z and 12z ECMWF IFS Ensemble Runs
        -----------------------------------
        
        3-Hourly Increments from hour 0 to hour 144.
        6-Hourly Increments from hour 144 to hour 360
        
        06z and 18z ECMWF IFS Ensemble Runs
        -----------------------------------
        
        3-Hourly Increments from hour 0 to hour 144.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

    7) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> ds = ecmwf_ifs_ens(proxies=proxies)
    
    8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    9) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Ensemble files will be saved to. 
        When set to None, the path will be: "ECMWF/IFS/ENSEMBLE/"
    
    13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    14) source (String) - Default='ecmwf'. The data server choice. When set to 'ecmwf' data is pulled from ecmwf-opendata.
        To switch to Amazon AWS, switch source='aws'. 
        
    15) level_type (String) - Default='surface'. The level of the parameters being queried. 
    
        level_types
        -----------
        
        1) 'surface'
        2) 'pressure'
        3) 'soil
    
    16) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    17) variables (String List) - Default is all variables. The list of variable names in plain-language. 
    
        variables
        ---------
        
        'Geopotential (step 0)'
        'Standard deviation of sub-gridscale orography (step 0)'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'maximum 10-meter wind gust step 0'
        'maximum 10-meter wind gust steps 3-144'
        '2-meter temperature'
        '2-meter dewpoint temperature'
        'mean sea level pressure'
        'mean zero-crossing wave period'
        'mean wave direction'
        'mean wave period'
        'peak wave period'
        'significant wave height'
        'runoff'
        'total precipitation'
        'surface pressure'
        'total column vertically integrated water vapor'
        'total cloud cover'
        'snow depth water equivalent'
        'snowfall water equivalent'
        'land sea mask'
        'volumetric soil moisture content'
        'soil temperature'
        'most unstable cape'
        'snow albedo'
        '3-hour minimum 2-meter temperature'
        '3-hour maximum 2-meter temperature'
        '6-hour minimum 2-meter temperature'
        '6-hour maximum 2-meter temperature'
        'total precipitation rate'
        'precipitation type'
        'top net longwave thermal radiation'
        'snow density'
        'surface net longwave thermal radiation'
        'surface net shortwave solar radiation'
        'surface shortwave radiation downward'
        'surface longwave radiation downward'
        'northward turbulent surface stress'
        'eastward turbulent surface stress'
        'eastward surface sea water velocity'
        'northward surface sea water velocity'
        'sea ice thickness'
        'sea surface height'
        'divergence'
        'geopotential height'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'relative vorticity'
        
    18) levels (Integer List) - Default=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]. 
        When level_type='pressure', this is the list of the pressure levels. 
        
        Example: User wants only the 500 mb level: levels=[500]
        
    19) members (Integer List) - Default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                          11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                          21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                          31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                          41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
                                          
        The ECMWF IFS Ensemble consists of 50 members. 
        
        Example: User wants only the first 5 members: members=[1,2,3,4,5]
            
    Returns
    -------
    
    An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys
    
    Plain Language ECMWF IFS Ensemble Variable Keys (After Post-Processing)
    --------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    '3_hr_maximum_2m_temperature'
    '3_hr_minimum_2m_temperature'
