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

from wxdata.utils.file_funcs import sorted_paths as _sorted_paths
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import shift_longitude as _shift_longitude

_sys.tracebacklimit = 0
_logging.disable()

def cfs_pressure_post_processing(path):
    
    """
    This function post-processes all GRIB2 Keys into a Plain Language Format for CFS Pressure Data.
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of CFS Pressure Data with variable keys decoded into plain-language.
    
    """
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'meanSea'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260080}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':3027}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260084}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'heightAboveGround'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'surface'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'paramId':260070}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'paramId':260071}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'tropopause'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'maxWind'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'heightAboveSea'}, 
                                backend_kwargs={"indexpath": ""})
        
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
                                filter_by_keys={'typeOfLevel': 'isothermZero'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds14 = _shift_longitude(ds14)
    except Exception as e:
        pass
    
    try:
        ds15 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds15 = _shift_longitude(ds15)
    except Exception as e:
        pass
    
    try:
        ds16 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds16 = _shift_longitude(ds16)
    except Exception as e:
        pass
    
    try:
        ds17 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'paramId': 59}, 
                                backend_kwargs={"indexpath": ""})
        
        ds17 = _shift_longitude(ds17)
    except Exception as e:
        pass
    
    try:
        ds18 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'paramId': 228001}, 
                                backend_kwargs={"indexpath": ""})
        
        ds18 = _shift_longitude(ds18)
    except Exception as e:
        pass
    
    try:
        ds19 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'sigmaLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds19 = _shift_longitude(ds19)
    except Exception as e:
        pass
    
    try:
        ds20 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'sigma'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds20 = _shift_longitude(ds20)
    except Exception as e:
        pass
    
    try:
        ds21 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'potentialVorticity'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds21 = _shift_longitude(ds21)
    except Exception as e:
        pass
    
    
    try:
        ds['mslp'] = ds['msl']
        ds = ds.drop_vars('msl')
    except Exception as e:
        pass
    
    try:
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds1['gh']
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds1['t']
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds1['r']
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds1['q']
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds1['w']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds1['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds1['v']
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds1['absv']
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds1['o3mr']
    except Exception as e:
        pass
    
    try:
        ds['stream_function'] = ds1['strf']
    except Exception as e:
        pass
    
    try:
        ds['velocity_potential'] = ds1['vp']
    except Exception as e:
        pass
    
    try:
        ds['5_wave_geopotential_height'] = ds2['wavh5']
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height_anomaly'] = ds3['gpa']
    except Exception as e:
        pass
    
    try:
        ds['5_wave_geopotential_height_anomaly'] = ds4['wava5']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds5['d2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds5['r2']
    except Exception as e:
        pass
    
    try:
        ds['total_precipitation'] = ds6['tp']
    except Exception as e:
        pass
    
    try:
        ds['total_convective_precipitation'] = ds6['acpcp']
    except Exception as e:
        pass
    
    try:        
        ds['total_non_convective_precipitation'] = ds6['ncpcp']
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_snow'] = ds6['csnow']
    except Exception as e:
        pass  
    
    try:
        ds['categorical_ice_pellets'] = ds6['cicep']
    except Exception as e:
        pass
    
    try: 
        ds['categorical_freezing_rain'] = ds6['cfrzr']
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds6['crain']
    except Exception as e:
        pass 
    
    try:        
        ds['surface_lifted_index'] = ds6['lftx']
    except Exception as e:
        pass 
    
    try:        
        ds['best_4_layer_lifted_index'] = ds6['lftx4']
    except Exception as e:
        pass    
    
    try:        
        ds['surface_cape'] = ds6['cape']
    except Exception as e:
        pass    
        
    try:        
        ds['surface_cin'] = ds6['cin']
    except Exception as e:
        pass 
    
    try:
        ds['cloud_water'] = ds7['cwat']
    except Exception as e:
        pass
    
    try:
        ds['entire_atmosphere_relative_humidity'] = ds7['r']
    except Exception as e:
        pass
    
    try:
        ds['total_ozone'] = ds7['tozne']
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds8['hlcy']
    except Exception as e:
        pass
    
    try:        
        ds['u_component_of_storm_motion'] = ds9['ustm']
    except Exception as e:
        pass     
       
    try:        
        ds['v_component_of_storm_motion'] = ds10['vstm']
    except Exception as e:
        pass    
    
    try:
        ds['tropopause_pressure'] = ds11['trpp']
    except Exception as e:
        pass
    
    try:
        ds['tropopause_height'] = ds11['gh']
    except Exception as e:
        pass
    
    try:        
        ds['tropopause_u_wind_component'] = ds11['u']
    except Exception as e:
        pass        
    
    try:        
        ds['tropopause_v_wind_component'] = ds11['v']
    except Exception as e:
        pass      
            
    try:        
        ds['tropopause_temperature'] = ds11['t']
    except Exception as e:
        pass    
              
    try:        
        ds['tropopause_vertical_speed_shear'] = ds11['vwsh']
    except Exception as e:
        pass  
    
    try:        
        ds['max_wind_u_component'] = ds12['u']
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_v_component'] = ds12['v']
    except Exception as e:
        pass   
    
    try:
        ds['max_wind_geopotential_height'] = ds12['gh']
    except Exception as e:
        pass
    
    try:
        ds['max_wind_pressure'] = ds12['pres']
    except Exception as e:
        pass
    
    try:
        ds['max_wind_temperature'] = ds12['t']
    except Exception as e:
        pass
    
    try:
        ds['temperature_height_above_sea'] = ds13['t']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds13['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds13['v']
    except Exception as e:
        pass
    
    try:        
        ds['zero_deg_c_isotherm_geopotential_height'] = ds14['gh']
    except Exception as e:
        pass       
           
    try:        
        ds['zero_deg_c_isotherm_relative_humidity'] = ds14['r']
    except Exception as e:
        pass 
    
    try:        
        ds['highest_tropospheric_freezing_level_geopotential_height'] = ds15['gh']
    except Exception as e:
        pass   
               
    try:        
        ds['highest_tropospheric_freezing_level_relative_humidity'] = ds15['r']
    except Exception as e:
        pass  
    
    try:
        ds['mixed_layer_temperature'] = ds16['t']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds16['r']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds16['q']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds16['u']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds16['v']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_dew_point'] = ds16['dpt']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_precipitable_water'] = ds16['pwat']
    except Exception as e:
        pass
    
    try:
        ds['parcel_lifted_index'] = ds16['pli']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cape'] = ds17['cape']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cin'] = ds18['cin']
    except Exception as e:
        pass
    
    try:
        ds['sigma_layer_relative_humidity'] = ds19['r']
    except Exception as e:
        pass
    
    try:        
        ds['995_sigma_temperature'] = ds20['t']
    except Exception as e:
        pass  
                
    try:        
        ds['995_sigma_theta'] = ds20['pt']
    except Exception as e:
        pass   
    
    try:        
        ds['995_sigma_relative_humdity'] = ds20['r']
    except Exception as e:
        pass       
    
    try:        
        ds['995_u_wind_component'] = ds20['u']
    except Exception as e:
        pass     
             
    try:        
        ds['995_v_wind_component'] = ds20['v']
    except Exception as e:
        pass    
              
    try:        
        ds['995_vertical_velocity'] = ds20['w']
    except Exception as e:
        pass 
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds21['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds21['v']
    except Exception as e:
        pass            
      
    try:        
        ds['potential_vorticity_level_temperature'] = ds21['t']
    except Exception as e:
        pass        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds21['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds21['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds21['vwsh']
    except Exception as e:
        pass    
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    
    return ds