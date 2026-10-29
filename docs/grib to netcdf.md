---
title: GRIB2 to NETCDF
---
# GRIB2 to NETCDF

```python
def grib_to_netcdf(ds,
                   path,
                   filename,
                   rtma=False):
```

This function converts an xarray.array in GRIB2 format transforms the xarray.array into a netCDF4 format and writes a
new netCDF (.nc) file consisting of the cleaned up data at {path}

Required Arguments:

1) ds (xarray.array) - The xarray.array dataset of GRIB2 data.

2) path (String) - The path to where the netCDF (.nc) file will be saved to.

3) filename (String) - The filename of the netCDF (.nc) file.

Optional Arguments:

1) rtma (Boolean) - Default=False. Set to True when working with RTMA data.
    Keep set to False when working with forecast model data. 

**Returns**

Saves a netCDF (.nc) file of the cleaned up GRIB2 data to {path}    
