"""
This file hosts the function responsible for GFS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""

import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import(
    clear_idx_files_in_path as _clear_idx_files_in_path,
    sorted_paths as _sorted_paths
)
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import(
    shift_longitude as _shift_longitude,
    convert_lon as _convert_lon
)

_sys.tracebacklimit = 0
_logging.disable()

def primary_gfs_post_processing(path,
                                western_bound,
                                eastern_bound,
                                southern_bound,
                                northern_bound):
    
    """
    This function post-processes the GFS0P25 and GFS0P50 GRIB Primary Variable Keys into Plain-Language Variable Keys
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of GFS0P25 data in Plain Language Keys.    
    
    Post-Process Variable Keys By Model
    -----------------------------------
    
    GFS0P25
    -------
    
    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
    'tropopause_u_wind_component'
    'tropopause_v_wind_component'
    'tropopause_temperature'
    'tropopause_vertical_speed_shear'
    'max_wind_u_component'
    'max_wind_v_component'
    'zero_deg_c_isotherm_geopotential_height'
    'zero_deg_c_isotherm_relative_humidity'
    'highest_tropospheric_freezing_level_geopotential_height'
    'highest_tropospheric_freezing_level_relative_humidity'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
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
    
    GFS0P50
    -------
    
    'mslp'
    'mslp_eta_reduction'
    'hybrid_level_cloud_mixing_ratio'
    'hybrid_level_ice_water_mixing_ratio'
    'hybrid_level_rain_mixing_ratio'
    'hybrid_level_snow_mixing_ratio'
    'hybrid_level_graupel'
    'hybrid_level_derived_radar_reflectivity'
    'boundary_layer_wind_u_component'
    'boundary_layer_wind_v_component'
    'ventilation_rate'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'total_cloud_cover'
    'ice_water_mixing_ratio'
    'rain_mixing_ratio'
    'cloud_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'derived_radar_reflectivity'
    '2m_temperature'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'low_level_u_wind_component'
    'low_level_v_wind_component'
    'low_level_temperature'
    'low_level_specific_humidity'
    'pressure_height_above_ground'
    '100m_u_wind_component'
    '100m_v_wind_component'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    'liquid_volumetric_soil_moisture_non_frozen'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'precipitable_water'
    'cloud_water'
    'entire_atmosphere_relative_humidity'
    'total_ozone'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'cloud_ceiling_height'
    'storm_relative_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'tropopause_height'
    'tropopause_u_wind_component'
    'tropopause_v_wind_component'
    'tropopause_temperature'
    'tropopause_vertical_speed_shear'
    'max_wind_u_component'
    'max_wind_v_component'
    'zero_deg_c_isotherm_geopotential_height'
    'zero_deg_c_isotherm_relative_humidity'
    'highest_tropospheric_freezing_level_geopotential_height'
    'highest_tropospheric_freezing_level_relative_humidity'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'mixed_layer_cape'
    'mixed_layer_cin'
    'pressure_level_from_which_a_parcel_was_lifted'
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
    """
    western_bound = eastern_bound = _convert_lon(western_bound, 
                                                 eastern_bound)
    
    _clear_idx_files_in_path(path)
    files = _sorted_paths(path)

    try:
        ds = _xr.open_mfdataset(files, 
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
        ds['mslp'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass  
    
    try:        
        ds['mslp_eta_reduction'] = ds['mslet']  
        ds = ds.drop_vars('mslet')
    except Exception as e:
        pass   
    
    try:        
        ds['cloud_mixing_ratio'] = ds['clwmr']
        ds = ds.drop_vars('clwmr')
    except Exception as e:
        pass      
    
    try:
        ds['ice_water_mixing_ratio'] = ds['icmr']  
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['rain_mixing_ratio'] = ds['rwmr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['snow_mixing_ratio'] = ds['snmr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds['grle']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['derived_radar_reflectivity'] = ds['refd']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['maximum_composite_reflectivity'] = ds['refc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['visibility'] = ds['vis']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['wind_gust'] = ds['gust']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['haines_index'] = ds['hindex']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['water_equivalent_of_accumulated_snow_depth'] = ds['sdwe']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:     
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:     
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass   
    
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:        
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass     
    
    try: 
        ds['categorical_snow'] = ds['csnow']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:
        ds['categorical_ice_pellets'] = ds['cicep']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try: 
        ds['categorical_freezing_rain'] = ds['cfrzr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds['crain']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:        
        ds['surface_roughness'] = ds['fsr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass        
    
    try:        
        ds['frictional_velocity'] = ds['fricv']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass      
        
    try:
        ds['vegetation'] = ds['veg']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['soil_type'] = ds['slt']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['wilting_point'] = ds['wilt']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass        
    
    try:        
        ds['field_capacity'] = ds['fldcp']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass       
     
    try:        
        ds['sunshine_duration'] = ds['SUNSD']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass     
       
    try:        
        ds['surface_lifted_index'] = ds['lftx']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass   
         
    try:        
        ds['best_4_layer_lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass    
    
    try:        
        ds['surface_cape'] = ds['cape']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass    
        
    try:        
        ds['surface_cin'] = ds['cin']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass 
    
    try:        
        ds['sea_ice_area_fraction'] = ds['siconc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass        
    
    try:
        ds['sea_ice_temperature'] = ds['sit']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_wind_u_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_wind_v_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['ventilation_rate'] = ds['VRATE']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds['wz']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass

    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds['o3mr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['ice_water_mixing_ratio'] = ds['clwmr']  
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['rain_mixing_ratio'] = ds['icmr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['cloud_mixing_ratio'] = ds['rwmr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass      
    
    try:
        ds['snow_mixing_ratio'] = ds['snmr']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds['grle']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['derived_radar_reflectivity'] = ds['refd']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds['r2']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['low_level_u_wind_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['low_level_v_wind_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['low_level_temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['low_level_specific_humidity'] = ds['q']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['pressure_height_above_ground'] = ds['pres']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['100m_u_wind_component'] = ds['u100']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['100m_v_wind_component'] = ds['v100']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['volumetric_soil_moisture_content'] = ds['soilw']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds['soill']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass    
    
    try:
        ds['temperature_height_above_sea'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['cloud_water'] = ds['cwat']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['entire_atmosphere_relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['total_ozone'] = ds['tozne']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_cover'] = ds['lcc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_cover'] = ds['mcc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
        
    try:
        ds['high_cloud_cover'] = ds['hcc']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['cloud_ceiling_height'] = ds['gh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds['hlcy']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['u_component_of_storm_motion'] = ds['ustm']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass     
       
    try:        
        ds['v_component_of_storm_motion'] = ds['vstm']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass      
    
    try:
        ds['tropopause_pressure'] = ds['trpp']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['tropopause_standard_atmosphere_reference_height'] = ds['icaht']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['tropopause_height'] = ds['gh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['tropopause_u_wind_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass        
    
    try:        
        ds['tropopause_v_wind_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass      
            
    try:        
        ds['tropopause_temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass    
              
    try:        
        ds['tropopause_vertical_speed_shear'] = ds['vwsh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_u_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_v_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass   
    
    try:        
        ds['zero_deg_c_isotherm_geopotential_height'] = ds['gh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass       
           
    try:        
        ds['zero_deg_c_isotherm_relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:        
        ds['highest_tropospheric_freezing_level_geopotential_height'] = ds['gh']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass   
               
    try:        
        ds['highest_tropospheric_freezing_level_relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
    
    try:
        ds['mixed_layer_temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds['q']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds['u']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds['v']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cape'] = ds['cape']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cin'] = ds['cin']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['pressure_level_from_which_a_parcel_was_lifted'] = ds['plpl']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['sigma_layer_relative_humidity'] = ds['r']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:        
        ds['995_sigma_temperature'] = ds['t']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass  
                
    try:        
        ds['995_sigma_theta'] = ds['pt']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass   
    
    try:        
        ds['995_sigma_relative_humdity'] = ds['r']
    except Exception as e:
        pass       
    
    try:        
        ds['995_u_wind_component'] = ds['u']
    except Exception as e:
        pass     
             
    try:        
        ds['995_v_wind_component'] = ds['v']
    except Exception as e:
        pass    
              
    try:        
        ds['995_vertical_velocity'] = ds['w']
    except Exception as e:
        pass 
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds['v']
    except Exception as e:
        pass            
        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds['vwsh']
    except Exception as e:
        pass    
    
    _clear_idx_files_in_path(path)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        pass
    
    return ds


def secondary_gfs_post_processing(path):
    
    """
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
    'air_temperature'
    'relative_humidity'
    'absolute_vorticity'
    'geopotential_height'
    'ozone_mixing_ratio'
    'total_cloud_cover'
    'cloud_mixing_ratio'
    'ice_water_mixing_ratio'
    'rain_water_mixing_ratio'
    'snow_mixing_ratio'
    'graupel'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'plant_canopy_surface_water'
    'sea_ice_thickness'
    'temperature_height_above_sea'
    'u_wind_component_height_above_sea'
    'v_wind_component_height_above_sea'
    'mixed_layer_temperature'
    'mixed_layer_relative_humidity'
    'mixed_layer_specific_humidity'
    'mixed_layer_u_wind_component'
    'mixed_layer_v_wind_component'
    'potential_vorticity_level_u_wind_component'
    'potential_vorticity_level_v_wind_component'
    'potential_vorticity_level_temperature'
    'potential_vorticity_level_geopotential_height'
    'potential_vorticity_level_air_pressure'
    'potential_vorticity_level_vertical_speed_shear' 
    
    """
    
    _clear_idx_files_in_path(path)
    files = _sorted_paths(path)

    try:
        ds = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
        
        ds = _shift_longitude(ds)
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260131})
        
        ds1 = _shift_longitude(ds1)
    except Exception as e:
        pass
    
    try:
        ds2 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':228164})
        
        ds2 = _shift_longitude(ds2)
    except Exception as e:
        pass
    
    try:
        ds3 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260018})
        
        ds3 = _shift_longitude(ds3)
    except Exception as e:
        pass
    
    try:
        ds4 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260019})
        
        ds4 = _shift_longitude(ds4)
    except Exception as e:
        pass
    
    try:
        ds5 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260020})
        
        ds5 = _shift_longitude(ds5)
    except Exception as e:
        pass
    
    try:
        ds6 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260021})
        
        ds6 = _shift_longitude(ds6)
    except Exception as e:
        pass
    
    try:
        ds7 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260028})
        
        ds7 = _shift_longitude(ds7)
    except Exception as e:
        pass
    
    try:
        ds8 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':135})
        
        ds8 = _shift_longitude(ds8)
    except Exception as e:
        pass
    
    try:
        ds9 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa','paramId':260238})
        
        ds9 = _shift_longitude(ds9)
    except Exception as e:
        pass
    
    try:
        ds10 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'})
        
        ds10 = _shift_longitude(ds10)
    except Exception as e:
        pass
    
    try:
        ds11 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'surface'})
        
        ds11 = _shift_longitude(ds11)
    except Exception as e:
        pass
    
    try:
        ds12 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'heightAboveSea'})
        
        ds12 = _shift_longitude(ds12)
    except Exception as e:
        pass
    
    try:
        ds13 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'})
        
        ds13 = _shift_longitude(ds13)
    except Exception as e:
        pass 
    
    try:
        ds14 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'potentialVorticity'})
        
        ds14 = _shift_longitude(ds14)
    except Exception as e:
        pass 
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('v')
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['vertical_speed_shear'] = ds['wvsh']
        ds = ds.drop_vars('wvsh')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds1['o3mr']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds2['tcc']
    except Exception as e:
        pass
    
    try:
        ds['cloud_mixing_ratio'] = ds3['clwmr']
    except Exception as e:
        pass
    
    try:
        ds['ice_water_mixing_ratio'] = ds4['icmr']
    except Exception as e:
        pass
    
    try:
        ds['rain_water_mixing_ratio'] = ds5['rwmr']
    except Exception as e:
        pass
    
    try:
        ds['snow_mixing_ratio'] = ds6['snmr']
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds7['grle']
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds8['w']
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds9['wz']
    except Exception as e:
        pass
    
    try:
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds10['soill']
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds11['cnwat']
    except Exception as e:
        pass
    
    try:
        ds['sea_ice_thickness'] = ds11['sithick']
    except Exception as e:
        pass
    
    try:
        ds['temperature_height_above_sea'] = ds12['t']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds12['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds12['v']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_temperature'] = ds13['t']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds13['r']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds13['q']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds13['u']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds13['v']
    except Exception as e:
        pass
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds14['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds14['v']
    except Exception as e:
        pass            
      
    try:        
        ds['potential_vorticity_level_temperature'] = ds14['t']
    except Exception as e:
        pass        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds14['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds14['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds14['vwsh']
    except Exception as e:
        pass    
    
    _clear_idx_files_in_path(path)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    
    return ds