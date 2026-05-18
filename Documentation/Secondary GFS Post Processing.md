# Secondary GFS Variables Post-Processing

***def secondary_gfs_post_processing(path,
                                western_bound,
                                eastern_bound,
                                southern_bound,
                                northern_bound):***

    This function post-processes the GFS0P25 and GFS0P50 GRIB Primary Variable Keys into Plain-Language Variable Keys
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of GFS0P25 data in Plain Language Keys.   
    
    Post-processed variable keys
    ----------------------------
    
    'u_wind_component'
    'v_wind_component'
    'temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'vertical_speed_shear'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'specific_humidity'
    'pressure'
