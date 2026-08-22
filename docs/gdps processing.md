---
title: GDPS Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Global Deterministic Prediction System (GDPS) Processing

```python
def gdps_post_processing(path,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound,
                         variable):
```
This function processes the model data from the GDPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.

2) Trimming the data to fit the coordinates of your bounding box.

3) Transform `ds['longitude']` from a 0 to 360 coordinate system to -180 to 180 for the GDPS.

Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the GDPS.

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) variable (String) - The name of the variable to rename our dataset with the proper variable key.  

Optional Arguments: None 

**Returns**

An `xarray.array` of the latest GDPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.
