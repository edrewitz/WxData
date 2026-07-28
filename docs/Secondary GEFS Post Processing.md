# Secondary GEFS Variables Post-Processing

***def secondary_gefs_post_processing(paths,
                                   western_bound,
                                   eastern_bound,
                                   southern_bound,
                                   northern_bound):***

    This function post-processes the GEFS (Secondary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) 1) paths (List) - A list of file paths to the GEFS0P50 Secondary Parameters. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    'temperature'
    'surface_visibility'
    'surface_wind_gust'
    'haines_index'
    'plant_canopy_surface_water'
    'snow_cover'
    'percent_frozen_precipitation'
    'snow_phase_change_heat_flux'
    'surface_roughness'
    'frictional_velocity'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'land_sea_mask'
    'sea_ice_area_fraction'
    'orography'
    'convective_precipitation_rate'
    'precipitation_rate'
    'total_convective_precipitation'
    'total_non_convective_precipitation'
    'total_precipitation'
    'water_runoff'
    'ground_heat_flux'
    'time_mean_u_component_of_atmospheric_surface_momentum_flux'
    'time_mean_v_component_of_atmospheric_surface_momentum_flux'
    'instantaneous_eastward_gravity_wave_surface_flux'
    'instantaneous_northward_gravity_wave_surface_flux'
    'uv_b_downward_solar_flux'
    'clear_sky_uv_b_downward_solar_flux'
    'average_surface_albedo'
    'mslp'
    'mslp_eta_reduction'  
    'ventilation_rate'
    'geopotential_height'
    'vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'ozone_mixing_ratio'
    'absolute_vorticity'
    'cloud_mixing_ratio'
    'icing_severity'
    'total_cloud_cover'
    'relative_humidity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_apparent_temperature'
    'specific_humidity'
    'pressure'
    'cloud_water'
    'total_ozone'
    'brightness_temperature'
    '3km_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'pressure'
    'tropopause_standard_atmosphere_reference_height'
    '995_sigma_theta'
    'potential_vorticity'
    'vertical_speed_shear'
    'theta_level_montgomery_potential'
    'potential_vorticity_level_vertical_speed_shear'
    'mixed_layer_dew_point'
    'mixed_layer_precipitable_water'
    'parcel_lifted_index_to_500hPa'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
