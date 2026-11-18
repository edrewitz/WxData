"""
This file hosts the post-processing for the WOOF-NAM Data.

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import sorted_paths as _sorted_paths
from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import shift_longitude as _shift_longitude


_eccodes_warning()
_sys.tracebacklimit = 0
_logging.disable()

def woof_nam_post_processing(path,
                             level_type):
    
    """
    
    
    """
    _eccodes_error_message()
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            backend_kwargs={"indexpath": ""})
        
        ds = _shift_longitude(ds,
                            x_y_dims=True)
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':156})
        
        ds1 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['geopotential_height'] = ds1['gh']
        ds = ds.drop_vars('gh')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':130})
        
        ds2 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['air_temperature'] = ds2['t']
        ds = ds.drop_vars('t')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':157})
        
        ds3 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['relative_humidity'] = ds3['r']
        ds = ds.drop_vars('r')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':135})
        
        ds4 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['vertical_velocity_pressure'] = ds4['w']
        ds = ds.drop_vars('w')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':131})
        
        ds5 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['u_wind_component'] = ds5['u']
        ds = ds.drop_vars('u')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':132})
        
        ds6 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['v_wind_component'] = ds6['v']
        ds = ds.drop_vars('v')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260155})
        
        ds7 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['turbulent_kinetic_energy'] = ds7['tke']
        ds = ds.drop_vars('tke')
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
                            backend_kwargs={"indexpath": ""},
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':3041})
        
        ds8 = _shift_longitude(ds,
                            x_y_dims=True)
        
        ds['absolute_vorticity'] = ds8['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass

    try:
        ds['vertical_velocity_height'] = ds['wz']
        ds = ds.drop_vars('wz')
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
        ds['derived_radar_reflectivity'] = ds['refd']
        ds = ds.drop_vars('refd')
    except Exception as e:
        pass
    
    try:
        ds['maximum_composite_reflectivity'] = ds['refc']
        ds = ds.drop_vars('refc')
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('pwat')
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
    except Exception as e:
        pass
    
    try:
        if level_type == 'surface':
            ds['planetary_boundary_layer_height'] = ds['unknown']
        elif level_type == 'entire atmosphere single layer':
            ds['radar_echo_top_height'] = ds['unknown']

        ds = ds.drop_vars('unknown')     
    except Exception as e:
        pass
    
       
    return ds