"""
This file hosts tools to help transform data to write new files with the cleaned up data.

(C) Eric J. Drewitz 2025-2026
"""
import os as _os 
import pandas as _pd

def grib_to_netcdf(ds,
                   path,
                   filename):
    
    """
    This function converts an xarray.array in GRIB2 format transforms the xarray.array into a netCDF4 format and writes a
    new netCDF (.nc) file consisting of the cleaned up data at {path}
    
    Required Arguments:
    
    1) ds (xarray.array) - The xarray.array dataset of GRIB2 data.
    
    2) path (String) - The path to where the netCDF (.nc) file will be saved to.
    
    3) filename (String) - The filename of the netCDF (.nc) file.
    
    **Returns**
    
    Saves a netCDF (.nc) file of the cleaned up GRIB2 data to {path}    
    """
    
    try:    
        if "dtype" in ds["step"].attrs:
            del ds["step"].attrs["dtype"]
        base_time = _pd.to_datetime(ds['time'].values)   

        new_time = base_time + _pd.to_timedelta(ds.step.values, unit="h")
        ds = ds.assign_coords(time=new_time)
        
        _os.makedirs(path, exist_ok=True)
        
        ds.to_netcdf(f"{path}/{filename}")
        
        print(f"{filename} saved to {path}")
    except Exception as e:
        _os.makedirs(path, exist_ok=True)
        
        ds.to_netcdf(f"{path}/{filename}")
        
        print(f"{filename} saved to {path}")