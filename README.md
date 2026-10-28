<img src="https://github.com/edrewitz/WxData/blob/main/icons/wxdata_logo.png.png?raw=true" width="400" height="400" alt="Alt text" />

***(C) Eric J. Drewitz 2025-2026***

[![Conda Recipe](https://img.shields.io/badge/recipe-wxdata-green.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) ![PyPI](https://img.shields.io/pypi/v/wxdata?label=pypi%20wxdata) 

[![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) 
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/license.svg)](https://anaconda.org/conda-forge/wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/wxdata) 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17727621.svg)](https://doi.org/10.5281/zenodo.17727621)

**Anaconda Downloads**

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata)


**PIP Downloads**

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/wxdata?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wxdata)


**WxData User Guide**

1) [What Is WxData?](https://edrewitz.github.io/WxData/#what-is-wxdata)

2) [Installation Instructions](https://edrewitz.github.io/WxData/#installation-instructions)

3) [WxData Documentation](https://edrewitz.github.io/WxData/#wxdata-documentation)
   
   1. [Current Weather Model Data Clients](https://edrewitz.github.io/WxData/#current-weather-model-data-clients)
      
   2. [Archived Weather Model Data Clients](https://edrewitz.github.io/WxData/#archived-weather-model-data-clients)
      
   3. [Command Line Interface & Shell Scripting](https://edrewitz.github.io/WxData/#command-line-interface--shell-scripting)
      
   4. [Raw Data Clients](https://edrewitz.github.io/WxData/#raw-data-clients)
      
   5. [Post-Processors](https://edrewitz.github.io/WxData/#post-processors)
       
   6. [Data Querying Tools](https://edrewitz.github.io/WxData/#data-querying-tools)
       
   7. [Data Transformation & Gap Filling Tools](https://edrewitz.github.io/WxData/#data-transformation--gap-filling-tools)
       
   8. [Automated Python Workflow Tools](https://edrewitz.github.io/WxData/#automated-python-workflow-tools)
       
   9. [Open-Meteo API](https://edrewitz.github.io/WxData/#open-meteo-api)

5) [WxData Tutorials](https://edrewitz.github.io/WxData/#wxdata-tutorials)

6) [Server List](https://edrewitz.github.io/WxData/#server-list)

7) [Citations](https://edrewitz.github.io/WxData/#citations)

8) [Data Sources](https://edrewitz.github.io/WxData/#data-sources)

**What is WxData?**

WxData is a Python package that has many clients for retrieving and processing various types of meteorological datasets (both real-time and archived) with a focus on automation. 
These datasets include 20+ Weather Forecast Models, Observational Data, Radar Data, Fuels Data (Fire Weather), Observed Upper-Air Sounding Data, Real-Time Mesoscale Analysis, Gridded NOAA National Weather Service Forecasts and Gridded NOAA Storm Prediction Center Outlooks, NOAA Climate Prediction Center Outlooks, as well as interfaces with the Open-Meteo and AirNow APIs. 

- WxData is also available in the command-line so users can write shell scripts to retrieve weather data. 

- WxData has support for server choice and rotation (if a server fails to respond) between the following:

   -  NCEP/NOMADS -> Amazon Web Services -> Google Cloud

   - ECMWF Open-Data -> Amazon Web Services -> Google Cloud

- WxData makes it easy for users to create automated ETL pipelines for their weather operations.

   - These automated ETL pipelines can be quite advanced (i.e. multiple concurrent GRIB2 file downloads between the main [i.e. NCEP/NOMADS] and cloud servers [i.e. AWS & Google Cloud] to spread the traffic between multiple servers (and you can use a proxy server if you choose) -> extracting an `xarray.array` from the GRIB2 files -> cleaning the `xarray.array` and decoding the GRIB2 variable keys into plain-language -> transforming & exporting the cleaned and decoded `xarray.array` into a NETCDF (.nc) file.    

- WxData supports GRIB -> NETCDF transformations.

- WxData decodes GRIB2 variable keys into plain-language and returns an `xarray.array` with the decoded variable keys.

- WxData has safeguards that prevent hitting server rate-limits.

- WxData has a medley of tools to query, fill gaps and transform data.

- WxData has additional tools to assist users with Python automated workflows. 

- WxData allows users who work on VPNs and behind firewalls to access data through a user-specified proxy server.

**Citations**

**MetPy**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
    Bruning, E. C., Manser, R. P., Arms, S. C., and Marsh, P. T., 2022: MetPy: A
    Meteorological Python Library for Data Analysis and Visualization. Bull. Amer. Meteor.
    Soc., 103, E2273-E2284, https://doi.org/10.1175/BAMS-D-21-0125.1.

**xarray**: Hoyer, S., Hamman, J. (In revision). Xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software.

**cartopy**: Phil Elson, Elliott Sales de Andrade, Greg Lucas, Ryan May, Richard Hattersley, Ed Campbell, Andrew Dawson, Bill Little, Stephane Raynaud, scmc72, Alan D. Snow, Ruth Comer, Kevin Donkers, Byron Blay, Peter Killick, Nat Wilson, Patrick Peglar, lgolston, lbdreyer, … Chris Havlin. (2023). SciTools/cartopy: v0.22.0 (v0.22.0). Zenodo. https://doi.org/10.5281/zenodo.8216315

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).

**Pandas**: Pandas: McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

**dask**: Dask Development Team (2016). Dask: Library for dynamic task scheduling. URL http://dask.pydata.org

**cfgrib**: Author: ECMWF, Year: (2025), Title: cfgrib: A Python interface to map GRIB files to xarray, Source: https://github.com/ecmwf/cfgrib 

**requests**: K. Reitz, "Requests: HTTP for Humans". Available: https://requests.readthedocs.io/.

**Beautiful Soup**: Richardson, L. (2025). Beautiful Soup (Version 4.14.3) [Computer software]. https://www.crummy.com/software/BeautifulSoup/

**shapeography**: Eric J. Drewitz. (2026). edrewitz/shapeography: shapeography 1.0 Released (shapeography1.0). Zenodo. https://doi.org/10.5281/zenodo.18676845

**geopandas**: Kelsey Jordahl, Joris Van den Bossche, Martin Fleischmann, Jacob Wasserman, James McBride, Jeffrey Gerard, … François Leblanc. (2020, July 15). geopandas/geopandas: v0.8.1 (Version v0.8.1). Zenodo. http://doi.org/10.5281/zenodo.3946761

**tqdm**: da Costa-Luis, (2019). tqdm: A Fast, Extensible Progress Meter for Python and CLI. Journal of Open Source Software, 4(37), 1277, https://doi.org/10.21105/joss.01277

**ecmwf-opendata**: European Centre for Medium-Range Weather Forecasts (2026). ecmwf-opendata[Computer software]. GitHub. https://github.com/ecmwf/ecmwf-opendata

**openpyxl**: Gazoni, E., & Clark, C. (2024). openpyxl: A Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files (Version 3.1.5) [Computer software]. https://openpyxl.readthedocs.io/

**pyart**: Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit (Py-ART), a Library for Working with Weather Radar Data in the Python Programming Language. Journal of Open Research Software. 4(1), p.e25. DOI: 10.5334/jors.119.

----------------------------------------------------------

**Data Sources**

1) [National Oceanic and Atmospheric Administration/National Center for Environmental Prediction](https://nomads.ncep.noaa.gov/)

2) [European Centre for Medium-Range Weather Forecasts](https://data.ecmwf.int/forecasts/)

3) [University of Wyoming](http://www.weather.uwyo.edu/upperair/sounding.shtml)

4) [National Oceanic and Atmospheric Administration/National Weather Service](https://tgftp.nws.noaa.gov/)

5) [National Oceanic and Atmospheric Administration/Aviation Weather Center](https://aviationweather.gov/)

6) [National Oceanic and Atmospheric Administration/Climate Prediction Center](https://www.cpc.ncep.noaa.gov/products/GIS/GIS_DATA/us_tempprcpfcst/index.php)

7) [Applied Climate Information System (ACIS)](https://www.rcc-acis.org/docs_webservices.html)

8) [USDA Fire Environment Mapping System](https://fems.fs2c.usda.gov/download)

9) [Open-Meteo API](https://open-meteo.com/)

10) [Air Now API](https://docs.airnowapi.org/webservices)

11) [Canadian Meteorological Centre](https://dd.weather.gc.ca/)

12) [Amazon Web Services](https://aws.amazon.com/)

13) [Google Cloud](https://cloud.google.com/)
