---
title: Shift Longitude
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# Shift Longitude
```python
def shift_longitude(ds, 
                    lon_name='longitude'):
```

Shifts longitude values to ensure continuity across the Prime Meridian.

Required Arguments:

1) ds (`xarray.data_array`) - The dataset of the model data.

Optional Arguments:

1) lon_name (String) - Default = longitude. The abbreviation for the longitude key.

Returns
-------

An `xarray.data_array` with longitude coordinates ranging from -180 to 180
