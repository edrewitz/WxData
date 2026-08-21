"""
This file hosts the function responsible for GDPS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import numpy as _np
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
   

def gdps_post_processing(path,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound,
                         variable):
    
    """
    This function processes the model data from the GDPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    2) Trimming the data to fit the coordinates of your bounding box.
    
    3) Transform ds['longitude'] from a 0 to 360 coordinate system to -180 to 180 for the GDPS.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    6) variable (String) - The name of the variable to rename our dataset with the proper variable key.  
    
    Optional Arguments: None 

    Returns
    -------    
    
    An xarray.array of the latest GDPS forecast data for a user-specified variable, level/layer and level_type.
    """


    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                eastern_bound) 

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                latitude=slice(southern_bound, northern_bound, 1))
        
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


def rdps_post_processing(path,
                         variable):
    
    """
    This function processes the model data from the RDPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
            
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    2) variable (String) - The name of the variable to rename our dataset with the proper variable key.
    
    Optional Arguments: None

    Returns
    -------    
    
    An xarray.array of the latest RDPS forecast data for a user-specified variable, level/layer and level_type.
    """

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(x=slice(180, 900, 1), 
                                                                      y=slice(0, 800, 1))
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

def hrdps_post_processing(path,
                         variable):
    
    """
    This function processes the model data from the HRDPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    2) variable (String) - The name of the variable to rename our dataset with the proper variable key.
    
    Optional Arguments: None

    Returns
    -------    
    
    An xarray.array of the latest HRDPS forecast data for a user-specified variable, level/layer and level_type.
    """

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""})
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


def cansips_post_processing(path,
                         variable,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound):
    
    """
    This function processes the model data from the CanSIPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    2) variable (String) - The name of the variable to rename our dataset with the proper variable key.
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.
    
    Optional Arguments: None

    Returns
    -------    
    
    An xarray.array of the latest CanSIPS data. 
    """
    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                eastern_bound) 

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                latitude=slice(southern_bound, northern_bound, 1))
        
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


