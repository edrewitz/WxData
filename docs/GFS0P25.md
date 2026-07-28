# GFS 0.25x0.25 Degree

***def gfs_0p25(final_forecast_hour=384, 
            western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            step=3,
            process_data=True,
            proxies=None, 
            variables=['geopotential height',
                       'temperature',
                       'relative humidity',
                       'u-component of wind'
                       'v-component of wind'],
            custom_directory=None,
            clear_recycle_bin=False,
            convert_temperature=True,
            convert_to='celsius',
            chunk_size=8192,
            notifications='off',
            clear_data=False,
            source='noaa',
            level_type='pressure',
            levels=[1000,
                    925,
                    850,
                    700,
                    500,
                    400,
                    300,
                    250,
                    200,
                    100,
                    50,
                    10]):***

    This function downloads GFS0P25 data and saves it to a folder. 
    
    Required Argumemnts: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P25
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 6 hours. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) step (Integer) - Default=3. Set to 3 for 3hr increments and 6 for 6hrly increments.
    
    7) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 

    8) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
       
    9) variables (String List) - Default=['geopotential height',
                                            'temperature',
                                            'relative humidity',
                                            'u-component of wind'
                                            'v-component of wind']
                       
        The variables the user wishes to query.
    
        Variables
        ---------
        
        'best lifted index'
        'absolute vorticity'
        'convective precipitation'
        'albedo'
        'total precipitation'
        'convective available potential energy'
        'categorical freezing rain'
        'categorical ice pellets'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'categorical rain'
        'categorical snow'
        'cloud water'
        'cloud work function'
        'downward longwave radiation flux'
        'dew point'
        'downward shortwave radiation flux'
        'vertical velocity (height)'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'graupel'
        'wind gust'
        'high cloud cover'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'ice growth rate'
        'ice thickness'
        'ice temperature'
        'ice water mixing ratio'
        'land cover'
        'low cloud cover'
        'surface lifted index'
        'latent heat net flux'
        'middle cloud cover'
        'mean sea level pressure'
        'mslp (eta model reduction)'
        'ozone mixing ratio'
        'potential evaporation rate'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'composite reflectivity'
        'reflectivity'
        'relative humidity'
        'rain mixing ratio'
        'surface roughness'
        'sensible heat net flux'
        'snow mixing ratio'
        'snow depth'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'soil type'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'upward longwave radiation flux'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'vegetation'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity (pressure)'
        'vertical speed shear'
        'water runoff'
        'water equivalent of accumulated snow depth'
        'wilting point'          
    
    10) custom_directory (String or None) - Default=None. If the user wishes to define their own directory to where the files are saved,
        the user must pass in a string representing the path of the directory. Otherwise, the directory created by default in WxData will
        be used. 
    
    11) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    12) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    13) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    14) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
        Default = f:ECMWF/IFS/WAVE
        
    15) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    16) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    17) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    18) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
        
    19) level_type (String) - Default='pressure'. The type of level for the variable.
    
        Level Types
        -----------
        
        'pressure'
        'mean sea level'
        'hybrid'
        'entire atmosphere'
        'boundary layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'convective cloud bottom level'
        'low cloud bottom level'
        'middle cloud bottom level'
        'high cloud bottom level'
        'convective cloud top level'
        'low cloud top level'
        'middle cloud top level'
        'high cloud top level'
        'convective cloud layer'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'height above ground'
        'surface'
        'height below ground'
        'sigma layer'
        'sigma level'
        'entire atmosphere (considered as a single layer)'
        'pressure above ground'
        'potential vorticity surface'
        
    20) levels (String, Integer or Float List) - Default=[1000,
                                                            925,
                                                            850,
                                                            700,
                                                            500,
                                                            400,
                                                            300,
                                                            250,
                                                            200,
                                                            100,
                                                            50,
                                                            10]   
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P25 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
