---
title: CanSIPS Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Processing

```python
def cansips_post_processing(path,
                         variable,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound):
```

This function processes the model data from the CanSIPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.

Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the CanSIPS.

2) variable (String) - The name of the variable to rename our dataset with the proper variable key.

3) western_bound (Float or Integer) - The western bound of the data needed. 

4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

5) northern_bound (Float or Integer) - The northern bound of the data needed.

6) southern_bound (Float or Integer) - The southern bound of the data needed.

Optional Arguments: None

**Returns**   

An `xarray.array` of the latest CanSIPS data. 
