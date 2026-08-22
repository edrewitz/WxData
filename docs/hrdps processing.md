---
title: HRDPS Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian High Resolution Deterministic Prediction System (HRDPS) Processing

```python
def hrdps_post_processing(path,
                         variable):
```

This function processes the model data from the HRDPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.

Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the HRDPS.

2) variable (String) - The name of the variable to rename our dataset with the proper variable key.

Optional Arguments: None

**Returns**

An `xarray.array` of the latest HRDPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.
