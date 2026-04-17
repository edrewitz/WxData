# Climate Forecast System (CFS) Flux

***def cfs_flux(western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            final_forecast_hour=384,
            proxies=None, 
            clear_recycle_bin=False,
            clear_data=False,
            chunk_size=8192,
            notifications='off',
            path=f"CFS/FLUX",
            process_data=True,
            convert_temperature=True,
            convert_to='celsius',
            variables=['aerodynamic conductance',
                        'albedo',
                        'clear sky uv-b downward solar flux',
                        'plant canopy surface water',
                        'convective precipitation rate',
                        'categorical rain',
                        'clear sky downward longwave flux',
                        'clear sky downward solar flux (surface)',
                        'clear sky downward solar flux (top of the atmosphere)',
                        'clear sky upward solar flux',
                        'cloud work function',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'clear sky uv-b downward solar flux',
                        'direct evaporation from bare soil',
                        'canopy water evaporation',
                        'surface friction velocity',
                        'ground heat flux',
                        'geopotential height',
                        'planetary boundary layer height',
                        'ice cover',
                        'ice thickness',
                        'land cover',
                        'latent heat net flux',
                        'near ir beam downward solar flux',
                        'near ir diffuse downward solar flux',
                        'potential evaporation rate',
                        'precipitation rate',
                        'pressure',
                        'precipitable water',
                        '2-meter maximum specific humidity',
                        '2-meter minimum specific humidity',
                        'sublimation (evaporation from snow)',
                        'surface roughness',
                        'sedimentation mass flux',
                        'sensible heat net flux',
                        'surface slope type',
                        'snow depth',
                        'snow phase-change heat flux',
                        'snow cover',
                        'liquid volumetric soil moisture (non-frozen)',
                        'soil moisture content',
                        'volumetric soil moisture content',
                        'soil type',
                        'specific humidity',
                        'snowfall rate water equivalent',
                        'storm surface runoff (non-infiltrating)',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'transpiration',
                        'momentum flux (u-component)',
                        'u-component of wind',
                        'zonal flux of gravity wave stress',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'visible beam downward solar flux',
                        'vegetation',
                        'momentum flux (v-component)',
                        'v-component of wind',
                        'vegetation type',
                        'meridional flux of gravity wave stress',
                        'water runoff',
                        'water equivalent of accumulated snow depth']):***

    This function is an end-to-end client that downloads, pre-processes, post-processes CFS Flux data.
    Post-processing remaps the variable keys from the coded GRIB format into a decoded Plain-Language Format
    
    Required Arguments: None.
    
    Optional Arguments:
    
    1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    5) final_forecast_hour (Integer) - Default=384. The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
        
    7) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin will be 
        deleted with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    8) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
        When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 
        
    9) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    10) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    11) path (String) - Default="CFS/PRESSURE". The path of the local directory where the files will be stored.
    
    12) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    13) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    14) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
                                
    15) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for CFS Flux
        -------------------------------
        
			'aerodynamic conductance'
            'albedo'
            'clear sky uv-b downward solar flux'
            'plant canopy surface water'
            'convective precipitation rate'
            'categorical rain'
            'clear sky downward longwave flux'
            'clear sky downward solar flux (surface)'
            'clear sky downward solar flux (top of the atmosphere)'
            'clear sky upward solar flux'
            'cloud work function'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'clear sky uv-b downward solar flux'
            'direct evaporation from bare soil'
            'canopy water evaporation'
            'surface friction velocity'
            'ground heat flux'
            'geopotential height'
            'planetary boundary layer height'
            'ice cover'
            'ice thickness'
            'land cover'
            'latent heat net flux'
            'near ir beam downward solar flux'
            'near ir diffuse downward solar flux'
            'potential evaporation rate'
            'precipitation rate'
            'pressure'
            'precipitable water'
            '2-meter maximum specific humidity'
            '2-meter minimum specific humidity'
            'sublimation (evaporation from snow)'
            'surface roughness'
            'sedimentation mass flux'
            'sensible heat net flux'
            'surface slope type'
            'snow depth'
            'snow phase-change heat flux'
            'snow cover'
            'liquid volumetric soil moisture (non-frozen)'
            'soil moisture content'
            'volumetric soil moisture content'
            'soil type'
            'specific humidity'
            'snowfall rate water equivalent'
            'storm surface runoff (non-infiltrating)'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'transpiration'
            'momentum flux (u-component)'
            'u-component of wind'
            'zonal flux of gravity wave stress'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'visible beam downward solar flux'
            'vegetation'
            'momentum flux (v-component)'
            'v-component of wind'
            'vegetation type'
            'meridional flux of gravity wave stress'
            'water runoff'
            'water equivalent of accumulated snow depth'
            
    Returns
    -------
    
    A post-processes xarray.array where the GRIB variable keys are decoded into a plain-language format.
    
    CFS Flux Data Variables In Plain-Language Format
    -------------------------------------------------
    
        'volumetric_soil_moisture_content'
        'soil_temperature'
        'liquid_volumetric_soil_moisture_non_frozen'
        'soil_moisture_content'
        'u_component_atmospheric_surface_momentum_flux'
        'v_component_atmospheric_surface_momentum_flux'
        'instantaneous_surface_sensible_heat_net_flux'
        'surface_latent_heat_net_flux'
        'surface_temperature'
        'water_equivalent_of_accumulated_snow_depth'
        'surface_downward_longwave_radiation_flux'
        'surface_upward_longwave_radiation_flux'
        'surface_upward_shortwave_radiation_flux'
        'surface_downward_shortwave_radiation_flux'
        'clear_sky_uv_b_downward_solar_flux'
        'precipitation_rate'
        'convective_precipitation_rate'
        'ground_heat_flux'
        'land_sea_mask'
        'sea_ice_area_fraction'
        'surface_pressure'
        'instantaneous_eastward_gravity_wave_surface_flux'
        'instantaneous_northward_gravity_wave_surface_flux'
        'surface_albedo'
        'sea_ice_thickness'
        'snow_depth'
        'plant_canopy_surface_water'
        'surface_roughness'
        'vegetation'
        'vegetation_type'
        'soil_type'
        'surface_slope_type'
        'frictional_velocity'
        'orography'
        'categorical_rain'
        'exchange_coefficient'
        'aerodynamic_conductance'
        'storm_surface_runoff'
        'direct_evaporation_from_bare_soil'
        'canopy_water_evaporation'
        'transpiration'
        'sublimation'
        'snow_cover'
        'clear_sky_downward_longwave_flux'
        'clear_sky_upward_solar_flux'
        'clear_sky_downward_solar_flux'
        'clear_sky_upward_longwave_flux'
        'snow_phase_change_heat_flux'
        'visible_beam_downward_solar_flux'
        'near_ir_beam_downward_solar_flux'
        'near_ir_diffuse_downward_solar_flux'
        'snowfall_rate_water_equivalent'
        'nominal_top_of_the_atmosphere_upward_longwave_radiation_flux'
        'nominal_top_of_the_atmosphere_upward_shortwave_radiation_flux'
        'nominal_top_of_the_atmosphere_downward_shortwave_radiation_flux'
        'nominal_top_of_the_atmosphere_clear_sky_upward_longwave_radiation_flux'
        'nominal_top_of_the_atmosphere_clear_sky_upward_solar_flux'
        'total_high_cloud_cover'
        'high_cloud_top_level_pressure'
        'high_cloud_top_level_temperature'
        'high_cloud_bottom_pressure'
        'total_middle_cloud_cover'
        'middle_cloud_top_level_pressure'
        'middle_cloud_top_level_temperature'
        'middle_cloud_bottom_pressure'
        'total_low_cloud_cover'
        'low_cloud_top_level_pressure'
        'low_cloud_top_level_temperature'
        'low_cloud_bottom_pressure'
        '10m_u_wind_component'
        '10m_v_wind_component'
        '2m_temperature'
        '2m_specific_humidity'
        'maximum_temperature'
        'minimum_temperature'
        'maximum_specific_humidity'
        'minimum_specific_humidity'
        'cloud_work_function'
        'precipitable_water'
        'total_cloud_cover'
        'total_convective_cloud_cover'
        'total_cloud_cover_boundary_layer'
        '995_sigma_temperature'
        '995_sigma_specific_humidity'
        '995_sigma_u_wind_component'
        '995_sigma_geopotential_height'   
