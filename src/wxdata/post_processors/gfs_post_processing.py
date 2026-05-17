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
    'ventilation_rate'
    'geopotential_height'
    'relative_humidity'
    'specific_humidity'
    'vertical_velocity'
    'geometric_vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'absolute_vorticity'
    'ozone_mixing_ratio'
    'total_cloud_cover'
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
    'tropopause_pressure'
    'tropopause_standard_atmosphere_reference_height'
    'vertical_speed_shear'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
    '995_sigma_theta'
        
    
    GFS0P50
    -------
    
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
        
    """
    # Returns an Error if pip was unable to install eccodes - This is an issue in latest versions of Python (>= 3.14)
    _eccodes_error_message()
    
    western_bound, eastern_bound = _convert_lon(western_bound, 
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
        ds['snow_mixing_ratio'] = ds['snmr']
        ds = ds.drop_vars('snmr')
    except Exception as e:
        pass
    
    try:
        ds['rain_mixing_ratio'] = ds['rwmr']
        ds = ds.drop_vars('rwmr')
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds['grle']
        ds = ds.drop_vars('grle')
    except Exception as e:
        pass
        
    try:
        ds['maximum_composite_reflectivity'] = ds['refc']
        ds = ds.drop_vars('refc')
    except Exception as e:
        pass
        
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
    except Exception as e:
        pass
        
    try:
        ds['visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass
        
    try:
        ds['wind_gust'] = ds['gust']
        ds = ds.drop_vars('gust')
    except Exception as e:
        pass
        
    try:
        ds['haines_index'] = ds['hindex']
        ds = ds.drop_vars('hindex')
    except Exception as e:
        pass
        
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass
        
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
        
    try:
        ds['temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('cnwat')
    except Exception as e:
        pass
    
    try:
        ds['water_equivalent_of_accumulated_snow_depth'] = ds['sdwe']
        ds = ds.drop_vars('sdwe')
    except Exception as e:
        pass
    
    try:     
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass  
    
    try:     
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('sithick')
    except Exception as e:
        pass   
    
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('cpofp')
    except Exception as e:
        pass  
    
    try:        
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('prate')
    except Exception as e:
        pass     
    
    try: 
        ds['categorical_snow'] = ds['csnow']
        ds = ds.drop_vars('csnow')
    except Exception as e:
        pass  
    
    try:
        ds['categorical_ice_pellets'] = ds['cicep']
        ds = ds.drop_vars('cicep')
    except Exception as e:
        pass
    
    try: 
        ds['categorical_freezing_rain'] = ds['cfrzr']
        ds = ds.drop_vars('cfrzr')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds['crain']
        ds = ds.drop_vars('crain')
    except Exception as e:
        pass  
    
    try:        
        ds['surface_roughness'] = ds['fsr']
        ds = ds.drop_vars('fsr')
    except Exception as e:
        pass        
    
    try:        
        ds['frictional_velocity'] = ds['fricv']
        ds = ds.drop_vars('fricv')
    except Exception as e:
        pass      
        
    try:
        ds['vegetation'] = ds['veg']
        ds = ds.drop_vars('veg')
    except Exception as e:
        pass
    
    try:
        ds['soil_type'] = ds['slt']
        ds = ds.drop_vars('slt')
    except Exception as e:
        pass
    
    try:        
        ds['wilting_point'] = ds['wilt']
        ds = ds.drop_vars('wilt')
    except Exception as e:
        pass        
    
    try:        
        ds['field_capacity'] = ds['fldcp']
        ds = ds.drop_vars('fldcp')
    except Exception as e:
        pass       
     
    try:        
        ds['sunshine_duration'] = ds['SUNSD']
        ds = ds.drop_vars('SUNSD')
    except Exception as e:
        pass     
       
    try:        
        ds['surface_lifted_index'] = ds['lftx']
        ds = ds.drop_vars('lftx')
    except Exception as e:
        pass   
         
    try:        
        ds['best_4_layer_lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('lftx4')
    except Exception as e:
        pass    
    
    try:        
        ds['sea_ice_area_fraction'] = ds['siconc']
        ds = ds.drop_vars('siconc')
    except Exception as e:
        pass        
    
    try:
        ds['sea_ice_temperature'] = ds['sit']
        ds = ds.drop_vars('sit')
    except Exception as e:
        pass
    
    try:
        ds['ventilation_rate'] = ds['VRATE']
        ds = ds.drop_vars('VRATE')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds['wz']
        ds = ds.drop_vars('wz')
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
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds['o3mr']
        ds = ds.drop_vars('o3mr')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('icmr')
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('sh2')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds['r2']
        ds = ds.drop_vars('r2')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('u10')
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('v10')
    except Exception as e:
        pass
    
    try:
        ds['pressure'] = ds['pres']
        ds = ds.drop_vars('pres')
    except Exception as e:
        pass
    
    try:
        ds['100m_u_wind_component'] = ds['u100']
        ds = ds.drop_vars('u100')
    except Exception as e:
        pass
    
    try:
        ds['100m_v_wind_component'] = ds['v100']
        ds = ds.drop_vars('v100')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('st')
    except Exception as e:
        pass
    
    try:        
        ds['volumetric_soil_moisture_content'] = ds['soilw']
        ds = ds.drop_vars('soilw')
    except Exception as e:
        pass
    
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds['soill']
        ds = ds.drop_vars('soill')
    except Exception as e:
        pass    
    
    try:
        ds['precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('pwat')
    except Exception as e:
        pass
    
    try:
        ds['cloud_water'] = ds['cwat']
        ds = ds.drop_vars('cwat')
    except Exception as e:
        pass
    
    try:
        ds['total_ozone'] = ds['tozne']
        ds = ds.drop_vars('tozne')
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_cover'] = ds['lcc']
        ds = ds.drop_vars('lcc')
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_cover'] = ds['mcc']
        ds = ds.drop_vars('mcc')
    except Exception as e:
        pass
        
    try:
        ds['high_cloud_cover'] = ds['hcc']
        ds = ds.drop_vars('hcc')
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds['hlcy']
        ds = ds.drop_vars('hlcy')
    except Exception as e:
        pass
    
    try:        
        ds['u_component_of_storm_motion'] = ds['ustm']
        ds = ds.drop_vars('ustm')
    except Exception as e:
        pass     
       
    try:        
        ds['v_component_of_storm_motion'] = ds['vstm']
        ds = ds.drop_vars('vstm')
    except Exception as e:
        pass      
    
    try:
        ds['tropopause_pressure'] = ds['trpp']
        ds = ds.drop_vars('trpp')
    except Exception as e:
        pass
    
    try:
        ds['tropopause_standard_atmosphere_reference_height'] = ds['icaht']
        ds = ds.drop_vars('icaht')
    except Exception as e:
        pass
              
    try:        
        ds['vertical_speed_shear'] = ds['vwsh']
        ds = ds.drop_vars('vwsh')
    except Exception as e:
        pass   
    
    try:
        ds['convective_available_potential_energy'] = ds['cape']
        ds = ds.drop_vars('cape')
    except Exception as e:
        pass
    
    try:
        ds['convective_inhibition'] = ds['cin']
        ds = ds.drop_vars('cin')
    except Exception as e:
        pass
    
    try:
        ds['pressure_level_from_which_a_parcel_was_lifted'] = ds['plpl']
        ds = ds.drop_vars('plpl')
    except Exception as e:
        pass
                
    try:        
        ds['995_sigma_theta'] = ds['pt']
        ds = ds.drop_vars('pt')
    except Exception as e:
        pass          
    
    _clear_idx_files_in_path(path)
    
    try:
        ds = ds.sortby('step')
    except Exception as e:
        pass
    
    return ds

def secondary_gfs_post_processing(path,
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

    
    """
    # Returns an Error if pip was unable to install eccodes - This is an issue in latest versions of Python (>= 3.14)
    _eccodes_error_message()
    
    western_bound, eastern_bound = _convert_lon(western_bound, 
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
        ds['temperature'] = ds['t']
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
        ds['ozone_mixing_ratio'] = ds['o3mr']
        ds = ds.drop_vars('o3mr')
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
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
        ds = ds.drop_vars('rwmr')
    except Exception as e:
        pass
    
    try:
        ds['snow_mixing_ratio'] = ds['snmr']
        ds = ds.drop_vars('snmr')
    except Exception as e:
        pass
    
    try:
        ds['graupel'] = ds['grle']
        ds = ds.drop_vars('grle')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass
    
    try:
        ds['geometric_vertical_velocity'] = ds['wz']
        ds = ds.drop_vars('wz')
    except Exception as e:
        pass
    
    try:
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds['soill']
        ds = ds.drop_vars('soill')
    except Exception as e:
        pass
    
    try:
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('cnwat')
    except Exception as e:
        pass
    
    try:
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('sithick')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass             
               
      
    try:        
        ds['pressure'] = ds['pres']
        ds = ds.drop_vars('pres')
    except Exception as e:
        pass       
    
    _clear_idx_files_in_path(path)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        pass
    
    return ds