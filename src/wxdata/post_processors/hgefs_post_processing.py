import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import file_paths_for_xarray as _file_paths_for_xarray
from wxdata.utils.coords import(
    shift_longitude as _shift_longitude,
    convert_lon as _convert_lon
)

_sys.tracebacklimit = 0
_logging.disable()

def _eccodes_error_intructions():
    
    """
    This function will print instructions if the user is using an incompatible Python environment with the eccodes C++ library.
    
    Known Errors:
    
    1) Using the pip version of eccodes with Python 3.14
    
    Fixes:
    
    1) Either downgrade the Python environment to be Python >= 3.10 and Python <= 3.13
    
    2) Install WxData via Anaconda rather than pip if the user must use Python >= 3.14
    
    Returns
    -------
    
    Instructions on how to resolve compatibility issues with the Python environment and eccodes.    
    """
    
    print("""
          Error: Incompatible Python version with the eccodes library.
          
          This is likely due to issues between Python >= 3.14 and eccodes
          
          Methods to fix:
          
          1) Uninstall the pip version of WxData and install WxData via Anaconda
             
             ***Steps For Method 1***
             1) pip uninstall wxdata
             2) conda install wxdata
             
          2) If the user is unable to use Anaconda as a package manager, the user must set up a new Python environment with the following specifications:
          
            ***Specifications***
            
            Python >= 3.10 and Python <= 3.13
            
            Python 3.10 is compatible.
            Python 3.11 is compatible.
            Python 3.12 is compatible.
            Python 3.13 is compatible
            
            Then pip install wxdata after the new Python environment is set up. 
            
          System Exiting...
          
          """)

def hgefs_mean_spread_post_processing(path,
                                western_bound,
                                eastern_bound,
                                northern_bound,
                                southern_bound):
    
    """
    This function post-processes the HGEFS Data into a more user-friendly format.
    
    Required Arguments:
    
    1) path (String) - The path to the HGEFS Data files.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array in a plain language variable key format.     
    
    Pressure-Level Plain Language Variable Keys
    -------------------------------------------
    
    'geopotential_height'
    'specific_humidity'
    'air_temperature'
    'u_wind_component'
    'v_wind_component'
    'vertical_velocity'
    
    Surface-Level Plain Language Variable Keys
    ------------------------------------------
    
    '10m_u_wind_component'
    '10m_v_wind_component'
    'mslp'
    '2m_temperature'
    'total_precipitation'
    """
    
    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                    eastern_bound) 
    
    path = _file_paths_for_xarray(path)
    
    try:
        ds = _xr.open_mfdataset(path, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False, 
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                            latitude=slice(northern_bound, southern_bound, 1))
        ds = _shift_longitude(ds)
        
        try:
            ds['10m_u_wind_component'] = ds['u10']
            ds = ds.drop_vars('u10')
        except Exception as e:
            pass
        
        try:
            ds['geopotential_height'] = ds['gh']
            ds = ds.drop_vars('gh')
        except Exception as e:
            pass
        
        try:
            ds['specific_humidity'] = ds['q']
            ds = ds.drop_vars('q')
        except Exception as e:
            pass
        
        try:
            ds['air_temperature'] = ds['t']
            ds = ds.drop_vars('t')
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
            ds['vertical_velocity'] = ds['w']
            ds = ds.drop_vars('w')
        except Exception as e:
            pass
        
        try:
            ds['total_precipitation'] = ds['tp']
            ds = ds.drop_vars('tp')
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
            ds['mslp'] = ds['prmsl']
            ds = ds.drop_vars('prmsl')
        except Exception as e:
            pass
        
        try:
            ds['total_precipitation'] = ds['tp']
            ds = ds.drop_vars('tp')
        except Exception as e:
            pass
        
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.open_mfdataset(path, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False, 
                                filter_by_keys={'paramId':167},
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                            latitude=slice(northern_bound, southern_bound, 1))
        ds1 = _shift_longitude(ds1)
        
        try:
            ds['2m_temperature'] = ds1['t2m']
        except Exception as e:
            pass
        
    except Exception as e:
        pass
    
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_intructions()
        _sys.exit(1)
    
    return ds