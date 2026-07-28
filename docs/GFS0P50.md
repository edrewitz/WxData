# GFS 0.5x0.5 Degree

***def gfs_0p50(final_forecast_hour=384, 
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
                    975,
                    950,
                    925,
                    900,
                    850,
                    800,
                    750,
                    700,
                    650,
                    600,
                    550,
                    500,
                    450,
                    400,
                    350,
                    300,
                    250,
                    200,
                    150,
                    100,
                    70,
                    50,
                    40,
                    30,
                    20,
                    15,
                    10,
                    7,
                    5,
                    3,
                    2,
                    1]):***

    This function downloads GFS0P50 data and saves it to a folder. 
    
    Required Argumemnts: None
    
    Optional Arguments:
    
    1) final_forecast_hour (Integer) - Default = 384. The final forecast hour the user wishes to download. The GFS0P50
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
        'clear sky uv-b downward solar flux'
        'uv-b downward solar flux'       
    
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
        
        
    20) levels (String, Integer or Float List) - Default=levels=[1000,
                                                                    975,
                                                                    950,
                                                                    925,
                                                                    900,
                                                                    850,
                                                                    800,
                                                                    750,
                                                                    700,
                                                                    650,
                                                                    600,
                                                                    550,
                                                                    500,
                                                                    450,
                                                                    400,
                                                                    350,
                                                                    300,
                                                                    250,
                                                                    200,
                                                                    150,
                                                                    100,
                                                                    70,
                                                                    50,
                                                                    40,
                                                                    30,
                                                                    20,
                                                                    15,
                                                                    10,
                                                                    7,
                                                                    5,
                                                                    3,
                                                                    2,
                                                                    1]
                                                            
        The pressure, height or depth levels.
    
    Returns
    -------
    
    An xarray.array dataset of the most recent GFS0P50 run. 
    
    Post-processed Variable Key List
    --------------------------------
    
    'mslp'
    'mslp_eta_reduction' 
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio' 
    'rain_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    'maximum_composite_reflectivity'
    'total_cloud_cover'
    'visibility'
    'wind_gust'
    'haines_index'
    'surface_pressure'
    'orography'
    'temperature'
    'plant_canopy_surface_water'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'percent_frozen_precipitation'
    'precipitation_rate'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'surface_roughness'
    'frictional_velocity'
    'vegetation'
    'soil_type'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'sea_ice_area_fraction'
    'sea_ice_temperature'
    'geopotential_height'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'pressure'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'precipitable_water'
    'cloud_water'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'vertical_speed_shear'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
    '995_sigma_theta'
