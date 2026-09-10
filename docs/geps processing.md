---
title: GEPS Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Canadian Global Ensemble Prediction System (GEPS) Processing

```python
def geps_post_processing(path,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound,
                         variable,
                         cat):
```

This function processes the model data from the GEPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.

2) Trimming the data to fit the coordinates of your bounding box.

3) Transform `ds['longitude']` from a 0 to 360 coordinate system to -180 to 180 for the GEPS.

Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the GEPS.

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) variable (String) - The name of the variable to rename our dataset with the proper variable key.  

7) cat (String) - Default='members'. Set `cat='members'` for all ensemble members OR set `cat='control'` for control run.

Optional Arguments: None 

**Returns**

An `xarray.array` of the latest GEPS forecast data for a user-specified variable, `level`/`layer` and `level_type`.
