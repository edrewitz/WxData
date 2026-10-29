"""
This file hosts the function responsible for CFS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""

import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import(
    shift_longitude as _shift_longitude,
    convert_lon as _convert_lon
)

_eccodes_warning()
_sys.tracebacklimit = 0
_logging.disable()

def cfs_post_processing(path,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound,
                         variable):
    
    """
    This function processes the model data from the CFS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    2) Trimming the data to fit the coordinates of your bounding box.
    
    3) Transform ds['longitude'] from a 0 to 360 coordinate system to -180 to 180 for the CFS.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data for the CFS.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) variable (String) - The name of the variable to rename our dataset with the proper variable key.  
    
        ***CFS Flux Data Variables In Plain-Language Format***

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
        
    ***CFS Pressure Data Variables In Plain-Language Format***
    
            'mslp'
            'geopotential_height'
            'air_temperature'
            'relative_humidity'
            'specific_humidity'
            'vertical_velocity'
            'u_wind_component'
            'v_wind_component'
            'absolute_vorticity'
            'ozone_mixing_ratio'
            'stream_function'
            'velocity_potential'
            '5_wave_geopotential_height'
            'geopotential_height_anomaly'
            '5_wave_geopotential_height_anomaly'
            '2m_dew_point'
            '2m_relative_humidity'
            'total_precipitation'
            'total_convective_precipitation'
            'total_non_convective_precipitation'
            'categorical_snow'
            'categorical_ice_pellets'
            'categorical_freezing_rain'
            'categorical_rain'
            'surface_lifted_index'
            'best_4_layer_lifted_index'
            'surface_cape'
            'surface_cin'
            'cloud_water'
            'entire_atmosphere_relative_humidity'
            'total_ozone'
            'storm_relative_helicity'
            'u_component_of_storm_motion'
            'v_component_of_storm_motion'
            'tropopause_pressure'
            'tropopause_height'
            'tropopause_u_wind_component'
            'tropopause_v_wind_component'
            'tropopause_temperature'
            'tropopause_vertical_speed_shear'
            'max_wind_u_component'
            'max_wind_v_component'
            'max_wind_geopotential_height'
            'max_wind_pressure'
            'max_wind_temperature'
            'temperature_height_above_sea'
            'u_wind_component_height_above_sea'
            'v_wind_component_height_above_sea'
            'zero_deg_c_isotherm_geopotential_height'
            'zero_deg_c_isotherm_relative_humidity'
            'highest_tropospheric_freezing_level_geopotential_height'
            'highest_tropospheric_freezing_level_relative_humidity'
            'mixed_layer_temperature'
            'mixed_layer_relative_humidity'
            'mixed_layer_specific_humidity'
            'mixed_layer_u_wind_component'
            'mixed_layer_v_wind_component'
            'mixed_layer_dew_point'
            'mixed_layer_precipitable_water'
            'parcel_lifted_index'
            'mixed_layer_cape'
            'mixed_layer_cin'
            'sigma_layer_relative_humidity'
            '995_sigma_temperature'
            '995_sigma_theta'
            '995_sigma_relative_humdity'
            '995_u_wind_component'
            '995_v_wind_component'
            '995_vertical_velocity'
            'potential_vorticity_level_u_wind_component'
            'potential_vorticity_level_v_wind_component'
            'potential_vorticity_level_temperature'
            'potential_vorticity_level_geopotential_height'
            'potential_vorticity_level_air_pressure'
            'potential_vorticity_level_vertical_speed_shear'
    
    Optional Arguments: None 

    Returns
    -------    
    
    An xarray.array of the latest CFS forecast data for a user-specified variable, level/layer and level_type.
    """


    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                eastern_bound) 

    try:
        ds = _xr.open_mfdataset(f"{path}/*grb2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                latitude=slice(northern_bound, southern_bound, 1))
            
        ds = _shift_longitude(ds)
    except Exception as e:
        pass
    
    
    try:
        var = str(list(ds.data_vars)[0])
        if ' ' in variable:
            variable = variable.replace(' ', '_')
        else:
            pass
        
        ds[variable] = ds[var]
        ds = ds.drop_vars(var)
    except Exception as e:
        pass

    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message() 

    try:
        ds = ds.drop_duplicates(dim='step', keep='first')
    except Exception as e:
        pass

    
    return ds