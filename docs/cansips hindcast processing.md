---
title: CanSIPS Hindcast Processing
---

[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)

# Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Hindcast Processing

```python
def cansips_hindcast_post_processing(path,
                         variable,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound):
```

This function processes the model data from the CanSIPS by doing the following:

1) Re-mapping the GRIB variable keys into a plain-language format.

2) Creating a 30-year mean of the hindcast data to use as a climatology for anomalies.

Process for calculating 30-year mean:

1) Find the ensemble mean for each year of the CanSIPS Hindcast data.

2) Find the time mean from all 30 ensemble means.

Required Arguments:

1) path (String) - The path to the directory holding the GRIB2 Data for the CanSIPS Hindcast data.
    This path should correspond to the parent directory of where the data is housed. In this directory,
    there are subdirectories corresponding to each year from 1991-2020 as we need to bin the files by year
    for proper ingestion. 

2) variable (String) - The name of the variable to rename our dataset with the proper variable key.

3) western_bound (Float or Integer) - The western bound of the data needed. 

4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

5) northern_bound (Float or Integer) - The northern bound of the data needed.

6) southern_bound (Float or Integer) - The southern bound of the data needed.

Optional Arguments: None

**Returns** 

An `xarray.array` of a 30-year mean CanSIPS Hindcast.  
