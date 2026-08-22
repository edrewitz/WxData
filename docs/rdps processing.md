---
title: RDPS Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Regional Deterministic Prediction System (RDPS) Processing

```python
def rdps_post_processing(path,
                         variable):
```
This function processes the model data from the RDPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.
        
Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the RDPS.

2) variable (String) - The name of the variable to rename our dataset with the proper variable key.

Optional Arguments: None

**Returns**

An `xarray.array` of the latest RDPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.
