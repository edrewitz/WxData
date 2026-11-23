---
title: WOOF-NAM Post-Processing
---
# WOOF-NAM Post-Processing

```python
def woof_nam_post_processing(path,
                             level_type):
```

This function processes the WOOF-NAM data into an xarray.array.

Required Arguments:

1) path (String) - The path to the directory where the data is being stored. 

2) level_type (String) - The type of level surface for the set of variables.

***Level Types***

```python
'mean sea level'
'hybrid'
'entire atmosphere single layer'
'surface'
'boundary layer'
'pressure'
'height above ground'
'depth below land layer'
'height below ground'
'lowest level wetbulb zero'
'isobaric layer'
'cloud base'
'height above ground layer (helicity)'
'height above ground layer (shear)'
'tropopause'
'max wind'
'isothermal'
'pressure above ground'
'sigma layer'
```

**Returns**

An xarray.array of the WOOF-NAM data for a specified level_type.     
